# benchmark_onnx_plus_stats.py
# Use if the input dimensions are dynamic to get flops
# python -m onnxruntime.tools.make_dynamic_shape_fixed  --input_name  input --input_shape 1,3,1920,1080 vsr_track2_ssr8c.onnx  vsr_track2_ssr8c_1080.onnx
# --------------------------------------------------------------
#
#  pip install onnx onnxruntime-gpu onnx_opcounter     #  ← Method A
#  # OR
#  pip install onnx onnxruntime-gpu onnx-tool          #  ← Method B
#
#  CUDA_VISIBLE_DEVICES=0 python benchmark_onnx_plus_stats.py \
#        --model video_model.onnx
# --------------------------------------------------------------

import argparse, time, numpy as np, onnx, torch, onnxruntime as ort

# ───────────────────────────────────
# (1) ----------  GPU session  ----------
# ───────────────────────────────────
def make_session(path, gpu_id=0):
    so = ort.SessionOptions()
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    providers = [("CUDAExecutionProvider", {"device_id": gpu_id}),
                 "CPUExecutionProvider"]
    return ort.InferenceSession(path, sess_options=so, providers=providers)  # 

# ───────────────────────────────────
# (2) ----  latency / throughput  ----
# ───────────────────────────────────
def latency(session, feed, warm=10, n=1000):
    for _ in range(warm):
        session.run(None, feed)
    samples = []
    for _ in range(n):
        t0 = time.perf_counter()
        session.run(None, feed)
        samples.append(time.perf_counter() - t0)
    return np.mean(samples) * 1e3  # ms

def throughput(session, feed, n_frames=1000):
    t0 = time.perf_counter()
    for _ in range(n_frames):
        session.run(None, feed)
    return n_frames / (time.perf_counter() - t0)

# ───────────────────────────────────
# (3) ------  params & FLOPs  -------
# ───────────────────────────────────
def model_stats(path, input_shapes=None, method="opcounter"):
    """
    Returns (#params, FLOPs).  If `input_shapes` is given (dict name→np.ndarray),
    FLOP counting takes actual tensor shapes into account (only in onnx-tool).
    """
    if method == "opcounter":
        # --- Method A: onnx_opcounter (static MAC counter) ---
        from onnx_opcounter import calculate_params, calculate_macs   # :contentReference[oaicite:1]{index=1}
        m = onnx.load(path)
        params = calculate_params(m)
        macs   = calculate_macs(m)
        flops  = macs * 2        # 1 MAC ≈ 2 FLOPs (mul + add)
        return params, flops

    elif method == "onnx_tool":
        # --- Method B: onnx-tool (handles dynamic shapes) ---
        import onnx_tool                                            # :contentReference[oaicite:2]{index=2}
        profile = onnx_tool.model_profile(path, input_shapes)  # returns dict‐like object
        params  = profile["total_params"]
        macs    = profile["total_macs"]
        return params, macs * 2

    else:
        raise ValueError("method must be 'opcounter' or 'onnx_tool'")

# ───────────────────────────────────
# (4) --------------  CLI -----------
# ───────────────────────────────────
TRACKS = [("track1", (1, 3, 180, 320)),
          ("track2", (1, 3, 272, 480)),
          ("track3", (1, 3, 360, 640))]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model",   required=True)
    ap.add_argument("--repeats", type=int, default=1000)
    ap.add_argument("--frames",  type=int, default=1000)
    ap.add_argument("--gpu",     type=int, default=0)
    ap.add_argument("--statlib", choices=["opcounter", "onnx_tool"], default="opcounter",
                    help="Library used for param/FLOP counting")
    args = ap.parse_args()

    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("CUDA is not available.")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


    sess = ort.InferenceSession(args.model, providers=["CPUExecutionProvider"])
    for i, inp in enumerate(sess.get_inputs()):
        print(f"[{i}] name={inp.name:20}  type={inp.type:10}  shape={inp.shape}")

    
    # -------- stats that do NOT depend on input resolution --------
    params, flops = model_stats(args.model, method=args.statlib)
    print(f"\nModel parameters : {params/1e6:,.2f} M")
    print(f"Theoretical FLOPs : {flops/1e9:,.2f} G (per forward, batch=1)\n")

    
    # -------- per-resolution benchmark --------
    sess = make_session(args.model, args.gpu)
    input_name = sess.get_inputs()[0].name

    for name, shape in TRACKS:
        print(f"=== {name}  {shape}")

        dummy = torch.randn(*shape, dtype=torch.float32).numpy()
        feed  = {input_name: dummy}

        lat = latency(sess, feed, n=args.repeats)
        fps = throughput(sess, feed, n_frames=args.frames)

        print(f"Latency   : {lat:.2f} ms  (mean of {args.repeats})")
        print(f"Throughput: {fps:.2f} FPS")
    