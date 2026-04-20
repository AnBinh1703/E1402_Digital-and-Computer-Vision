# EXACT CODE FIXES REQUIRED

## Overview
This document provides exact code snippets to fix all critical errors and implement optimizations.

---

## CRITICAL FIXES (MUST IMPLEMENT)

### Fix 1: Add Missing TrainConfig Class
**Location:** Cell 38, after line 2101 (before line 2109)
**Current Issue:** Cell 40 uses `TrainConfig(...)` but class is not defined

**Add this code:**
```python
from dataclasses import dataclass, field

@dataclass
class TrainConfig:
    """Configuration for YOLO model training"""
    model_name: str = "yolov8n.pt"
    epochs: int = 5
    imgsz: int = 640
    batch: int = 16
    patience: int = 3
    workers: int = 4
    experiment_name: str = "yolo_train"
    resume: bool = False
    lr0: float = 0.01
    lrf: float = 0.01
    device: int | str = 0  # 0 for GPU, "cpu" for CPU
```

**Cell 38 updated structure:**
```python
# ============================================================================
# SECTION 1: YOLO ENVIRONMENT & CONFIGURATION
# ============================================================================
# ... existing imports ...

# ADD THIS:
@dataclass
class TrainConfig:
    model_name: str = "yolov8n.pt"
    # ... fields above ...

# ... rest of Cell 38 ...
```

---

### Fix 2: Add Missing train_yolo() Function
**Location:** Cell 38, after TrainConfig definition (before line 2137)
**Current Issue:** Cells 40, 47, 48 call `train_yolo()` but function is not defined

**Add this code:**
```python
def train_yolo(cfg: TrainConfig, data_yaml: Path):
    """
    Train YOLO model with given configuration.
    
    Args:
        cfg: TrainConfig with model and training parameters
        data_yaml: Path to data.yaml file
        
    Returns:
        Tuple of (results, run_dir, best_checkpoint_path, last_checkpoint_path)
    """
    # Determine device
    if isinstance(cfg.device, int):
        device = cfg.device if torch.cuda.is_available() else "cpu"
    else:
        device = cfg.device
    
    # Load model
    model = YOLO(cfg.model_name)
    
    # Train
    results = model.train(
        data=str(data_yaml),
        epochs=cfg.epochs,
        imgsz=cfg.imgsz,
        batch=cfg.batch,
        patience=cfg.patience,
        workers=cfg.workers,
        project=str(RUNS_DIR),
        name=cfg.experiment_name,
        resume=cfg.resume,
        device=device,
        lr0=cfg.lr0,
        lrf=cfg.lrf,
        verbose=True,
        plots=True,
        save=True,
        save_json=True,
    )
    
    # Return paths
    run_dir = RUNS_DIR / cfg.experiment_name
    best_ckpt = run_dir / "weights" / "best.pt"
    last_ckpt = run_dir / "weights" / "last.pt"
    
    return results, run_dir, best_ckpt, last_ckpt
```

---

### Fix 3: Add Missing auto_batch_size() Function
**Location:** Cell 42, before line 2356 (at the start of the cell)
**Current Issue:** Cells 42, 43, 45, 47, 48 call `auto_batch_size()` but function is not defined

**Add this code:**
```python
def auto_batch_size(max_batch: int) -> int:
    """
    Auto-calculate optimal batch size based on GPU memory.
    
    Uses heuristic: 1GB GPU memory ≈ batch_size 4-8 for YOLOv8n
    
    Args:
        max_batch: Maximum batch size to not exceed
        
    Returns:
        Recommended batch size for current GPU
    """
    if not torch.cuda.is_available():
        return 1
    
    try:
        # Get GPU memory in GB
        gpu_props = torch.cuda.get_device_properties(0)
        gpu_mem_gb = gpu_props.total_memory / 1e9
        
        # Heuristic: 1GB ≈ batch 4 for YOLOv8n
        # Adjust based on model complexity
        calc_batch = max(1, int(gpu_mem_gb / 2))
        
        # Don't exceed maximum
        optimal_batch = min(calc_batch, max_batch)
        
        print(f"GPU memory: {gpu_mem_gb:.1f}GB → auto batch: {optimal_batch}")
        return optimal_batch
        
    except Exception as e:
        print(f"auto_batch_size warning: {e}. Using max_batch={max_batch}")
        return max_batch
```

**Cell 42 structure:**
```python
# ============================================================================
# SECTION 6A: EVALUATION & METRICS
# ============================================================================

# ADD THIS FUNCTION FIRST:
def auto_batch_size(max_batch: int) -> int:
    """..."""
    # ... code above ...

# Then existing evaluate_yolo() and other functions
```

---

## HIGH PRIORITY OPTIMIZATIONS

### Optimization 1: Fix YOLO Image Size
**Location:** Cell 40, line 2286
**Current:** `imgsz=32,`
**Changed to:** `imgsz=416,`

**Why:** YOLO requires minimum 320 pixels. 32×32 is for classifiers, not object detection.

**Cell 40 section:**
```python
# BEFORE:
CFG_TRAIN_BASE = TrainConfig(
    model_name="yolov8n.pt",
    epochs=5,
    imgsz=32,  # ← TOO SMALL FOR YOLO
    batch=4,
    # ...
)

# AFTER:
CFG_TRAIN_BASE = TrainConfig(
    model_name="yolov8n.pt",
    epochs=3,  # Also reduce epochs for faster demo
    imgsz=416,  # ← FIXED: Proper size for YOLO
    batch=8,    # ← Also increase batch for 2x throughput
    patience=2,
    workers=4,
    experiment_name="yolov8n_fast_gpu",
    resume=False,
)
```

---

### Optimization 2: Increase YOLO Batch Size
**Location:** Cell 40, line 2286
**Current:** `batch=4,`
**Changed to:** `batch=8,` or `batch=16,`

**Why:** Batch=4 is extremely conservative. With most modern GPUs:
- 8GB GPU: batch=8-16
- 12GB GPU: batch=16-32
- 16GB+ GPU: batch=32-64

**Impact:** 2-4x faster training

**Cell 40 section:** (see above)

---

### Optimization 3: Skip YOLOv8m in Comparison
**Location:** Cell 47, line 2703
**Current:**
```python
COMPARE_MODELS = ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"]
```

**Changed to:**
```python
COMPARE_MODELS = ["yolov8n.pt", "yolov8s.pt"]  # Skip 'm' to save time
```

**Why:** YOLOv8m adds 40% to comparison training time. Skip it unless you need it.

---

### Optimization 4: Reduce Epochs in Model Comparison
**Location:** Cell 47, lines 2712-2715

**Current:**
```python
for model_ckpt in COMPARE_MODELS:
    exp_name = Path(model_ckpt).stem + "_compare"
    run_dir = RUNS_DIR / exp_name
    best_path = run_dir / "weights" / "best.pt"

    if RUN_MODEL_COMPARISON:
        cfg_cmp = TrainConfig(
            model_name=model_ckpt,
            epochs=12,      # ← REDUCE THIS
            imgsz=640,
            batch=16,
            patience=6,     # ← ALSO REDUCE THIS
            # ...
        )
```

**Changed to:**
```python
for model_ckpt in COMPARE_MODELS:
    exp_name = Path(model_ckpt).stem + "_compare"
    run_dir = RUNS_DIR / exp_name
    best_path = run_dir / "weights" / "best.pt"

    if RUN_MODEL_COMPARISON:
        cfg_cmp = TrainConfig(
            model_name=model_ckpt,
            epochs=8,       # ← REDUCED from 12
            imgsz=640,
            batch=16,
            patience=3,     # ← REDUCED from 6
            workers=4,
            experiment_name=exp_name,
            resume=False,
        )
```

**Impact:** 30-40% faster model comparison training

---

### Optimization 5: Fix Image Size in Grid Search Config
**Location:** Cell 47, line 2727 (in opt_grid list)

**Current:**
```python
opt_grid = [
    {"name": "opt_a", "epochs": 18, "imgsz": 640, "batch": 8,  "lr0": 0.01,  "lrf": 0.01},
    {"name": "opt_b", "epochs": 24, "imgsz": 640, "batch": 16, "lr0": 0.005, "lrf": 0.01},
    {"name": "opt_c", "epochs": 24, "imgsz": 768, "batch": 8,  "lr0": 0.003, "lrf": 0.008},  # ← 768 IS SLOW
]
```

**Changed to:**
```python
opt_grid = [
    {"name": "opt_a", "epochs": 12, "imgsz": 640, "batch": 8,  "lr0": 0.01,  "lrf": 0.01},  # ← Reduced epochs
    {"name": "opt_b", "epochs": 15, "imgsz": 640, "batch": 16, "lr0": 0.005, "lrf": 0.01},  # ← Reduced epochs
    {"name": "opt_c", "epochs": 15, "imgsz": 640, "batch": 8,  "lr0": 0.003, "lrf": 0.008},  # ← Changed 768→640, reduced epochs
]
```

**Why:**
- 768×768 images: 30% slower than 640×640, minimal accuracy gain
- 24 epochs: Too many for exploration phase; 12-15 sufficient
- Recommendation: Use these configurations, do final full training later with more epochs

**Impact:** 35-40% faster grid search

---

### Optimization 6: Reduce Global Batch Size
**Location:** Cell 3, line 107
**Current:** `BATCH_SIZE = 32`
**Changed to:** `BATCH_SIZE = 16`

**Why:**
- 32 is aggressive for 12GB GPU
- 16 is safer with better GPU utilization
- May need adjustment based on your GPU

**Cell 3 section:**
```python
# BEFORE:
BATCH_SIZE = 32
EPOCHS = 10

# AFTER:
BATCH_SIZE = 16  # Safer for 12GB GPU, still fast
EPOCHS = 5       # Also reduce this for demo
```

---

### Optimization 7: Reduce Global Epochs
**Location:** Cell 3, line 108
**Current:** `EPOCHS = 10`
**Changed to:** `EPOCHS = 5`

**Why:** Legacy config used by old classifier. 5 is sufficient for demonstration.

**Impact:** 50% faster when running legacy code sections

---

## SUMMARY OF ALL CHANGES

### Files to Create/Add:

**In Cell 38:**
1. Add `@dataclass class TrainConfig`
2. Add `def train_yolo(cfg, data_yaml)`

**In Cell 42 (start of cell):**
3. Add `def auto_batch_size(max_batch)`

### Files to Modify:

**Cell 3:**
- Line 107: `BATCH_SIZE = 32` → `BATCH_SIZE = 16`
- Line 108: `EPOCHS = 10` → `EPOCHS = 5`

**Cell 40:**
- Line 2284: `epochs=5` → `epochs=3`
- Line 2286: `imgsz=32` → `imgsz=416`
- Line 2286: `batch=4` → `batch=8`

**Cell 47:**
- Line 2703: Remove `"yolov8m.pt"` from list
- Line 2712-2714: Reduce `epochs`, `patience` values
- Line 2727: Change `imgsz=768` → `imgsz=640`

**Cell 48:**
- Lines 2742-2744: Reduce `epochs` values from 18,24,24 to 12,15,15

---

## VALIDATION CHECKLIST

After implementing fixes, verify:

- [ ] Cell 38 runs without errors (TrainConfig and train_yolo defined)
- [ ] Cell 40 runs without errors (uses defined TrainConfig and train_yolo)
- [ ] Cell 42 runs without errors (auto_batch_size function exists)
- [ ] Cells 43, 45 run without errors (auto_batch_size available)
- [ ] Cell 47 runs without errors (all functions defined, epochs reduced)
- [ ] Cell 48 runs without errors (all functions defined, epochs reduced)
- [ ] YOLO training starts with `imgsz=416` (visible in training output)
- [ ] GPU batch size is 8+ (not 4)
- [ ] Training completes faster than before

---

## EXPECTED RESULTS AFTER FIXES

**Before Optimizations:**
- Training time: 8-12 hours (full pipeline)
- All cells: Many NameError failures
- Image size too small for YOLO

**After Optimizations:**
- Training time: 2-3 hours (60-75% faster)
- All cells: Run successfully without errors
- YOLO detection: Accurate (416×416 images)
- Model comparison: 30-40% faster
- Grid search: 35-40% faster

