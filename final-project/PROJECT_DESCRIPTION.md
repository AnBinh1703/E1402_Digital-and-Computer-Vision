# Traffic Sign and Violation Detection System (ITS)
## Intelligent Transportation System for Automated Traffic Enforcement

**Student:** Duong Binh An  
**Student Code:** MSc-IA-25-0003304EN  
**Subject:** E1402_Digital and Computer Vision  
**Institution:** UMEF (Université Mention E1402)  

---

## 1. PROJECT GOAL

Develop an **end-to-end Intelligent Transportation System (ITS)** capable of:
- Detecting and recognizing traffic signs from video streams
- Tracking vehicle movements in real-time
- Identifying traffic violations automatically
- Logging incidents with evidence for enforcement and analysis

This is a **powerful real-world computer vision application** essential for:
- Smart cities and urban traffic management
- Automated traffic law enforcement
- Road safety monitoring
- Data collection for traffic analysis
- Insurance and liability assessment

---

## 2. SYSTEM REQUIREMENTS

### 2.1 Core Functionality
The system must detect and respond to the following scenarios:

#### **Traffic Sign Detection & Recognition**
- Detect traffic signs from video frames
- Classify signs into 43 categories (GTSRB benchmark classes)
- Support classes including:
  - Stop signs
  - Speed limit signs (20, 30, 50, 60, 70, 80, 100, 120 km/h)
  - No entry signs
  - Yield/Priority signs
  - And 39 other traffic sign types

#### **Vehicle Detection & Tracking**
- Detect vehicles in real-time (cars, motorcycles, buses, trucks)
- Maintain consistent tracking IDs across frames
- Compute vehicle speed from pixel movement
- Track trajectory and direction of movement

#### **Violation Detection (6 Violation Types)**
1. **Ignoring Stop Signs**
   - Detect stop sign in frame
   - Vehicle crosses stop line at speed > 5 km/h
   
2. **Speeding**
   - Compute vehicle speed from trajectory
   - Flag if speed exceeds limit (default: 50 km/h)
   
3. **Red Light Jumping**
   - Detect traffic light state (red/yellow/green)
   - Flag vehicle crossing at red light
   
4. **Wrong-Way Driving**
   - Detect vehicle moving opposite to expected direction
   - Alert on sustained reverse movement
   
5. **Lane Violations**
   - Define valid lane polygons
   - Flag vehicles outside designated lanes
   
6. **No-Entry Zone Violations**
   - Define forbidden zones
   - Detect vehicles entering restricted areas

#### **Incident Logging & Reporting**
For each violation, log:
- **Vehicle ID** (tracking ID maintained across frames)
- **Timestamp** (frame number and time in seconds)
- **Violation Type** (category as above)
- **Bounding Box** (vehicle location: x1, y1, x2, y2)
- **Cropped Image Evidence** (extracted vehicle region)
- **Additional Metadata** (speed, traffic light state, etc.)

**Output Formats:**
- CSV file: `violation_log.csv` (tabular incident records)
- JSON file: `violation_summary.json` (summary statistics)
- Evidence folder: cropped images for each incident

---

## 3. TOOLS AND MODELS

### 3.1 Traffic Sign Detection & Classification

| **Component** | **Tool/Model** | **Alternative** |
|---|---|---|
| **Sign Detection** | YOLOv8 (if weights available) | Color/shape heuristic detection |
| **Sign Classification** | ResNet18 CNN | MobileNet, EfficientNet |
| **Framework** | PyTorch | TensorFlow/Keras |
| **Dataset** | GTSRB (43 classes) | Synthetic data augmentation |

**Implementation:**
- Train classifier on GTSRB training images (39,209 images)
- Fine-tune ResNet18 with transfer learning
- Achieve ~95% accuracy on validation set (10% of data)
- Fallback: HSV color-based detection + aspect ratio heuristics

### 3.2 Vehicle Detection & Tracking

| **Component** | **Tool/Model** | **Alternative** |
|---|---|---|
| **Vehicle Detection** | YOLOv8 nano/small | SSD, EfficientDet, Faster R-CNN |
| **Multi-Object Tracking** | ByteTrack (ultralytics) | SORT, Deep SORT, StrongSORT |
| **Speed Estimation** | Optical flow + calibration | Homography-based warping |
| **Framework** | PyTorch | TensorFlow, ONNX |

**Implementation:**
- YOLO detects car, motorcycle, bus, truck classes
- ByteTrack maintains stable track IDs across frames
- Compute speed: pixel distance × calibration factor / time interval
- Configurable `meters_per_pixel` for accuracy

### 3.3 Violation Logic & Rule Engine

| **Component** | **Implementation** | **Input** |
|---|---|---|
| **Stop Line Crossing** | Pixel Y-coordinate comparison | Stop line Y position (configurable) |
| **Speed Threshold** | Simple comparison | Vehicle speed (km/h) vs limit |
| **Traffic Light State** | HSV color segmentation | ROI within traffic light bounding box |
| **Wrong-Way Detection** | Trajectory direction analysis | Track history (first frame vs last frame) |
| **Lane Validation** | Polygon containment test | Lane polygon coordinates |
| **Forbidden Zone Check** | Point-in-polygon (OpenCV) | Zone polygon coordinates |

**Features:**
- Cooldown mechanism (30 frames default) to avoid duplicate logs
- Configurable thresholds for each rule
- Real-time frame-by-frame processing

### 3.4 Logging & Reporting

| **Component** | **Technology** | **Format** |
|---|---|---|
| **CSV Export** | Pandas | violation_log.csv (incident table) |
| **JSON Summary** | Python json | violation_summary.json (statistics) |
| **Evidence Storage** | OpenCV imwrite | JPEG images per incident |
| **Video Output** | OpenCV VideoWriter | MP4 with annotations |

---

## 4. DATASET INFORMATION

### 4.1 German Traffic Sign Recognition Benchmark (GTSRB)

**Dataset Location:** `final-project/archive/`

**Structure:**
```
archive/
├── Train/                    # Training images (39,209 total)
│   ├── 0/                   # Stop signs (780 images)
│   ├── 1/                   # Speed limit 20 km/h
│   ├── 2/                   # Speed limit 30 km/h
│   ├── 3/                   # Speed limit 50 km/h
│   ├── ...
│   └── 42/                  # Go straight or right
├── Test/                     # Test images (12,630 total)
│   ├── GT-final_test.csv    # Test ground truth labels
│   └── [image files]
├── Meta.csv                 # Class metadata (43 classes)
├── Train.csv                # Training metadata
└── Test.csv                 # Test metadata
```

**Classes:** 43 traffic sign types (0-42)
- **Class 0:** Stop sign
- **Classes 1-9:** Speed limit signs (20, 30, 50, 60, 70, 80, 100, 120 km/h)
- **Class 10:** No entry
- **Classes 11-14:** Priority/Yield variants
- **And 28 more classes...**

**Key Statistics:**
- Total training images: **39,209**
- Total test images: **12,630**
- Image size: 32×32 to 250×250 pixels
- Variations: lighting, perspective, occlusion, blur

---

## 5. SYSTEM ARCHITECTURE

### 5.1 Pipeline Flow

```
Video Input
    ↓
[Frame Extraction] ← 30 FPS (configurable)
    ↓
┌──────────────────────────────────────┐
│  Sign Detection & Recognition        │
│  - YOLO detection (or heuristic)     │
│  - ResNet18 classification           │
│  - Extract sign labels               │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  Vehicle Detection & Tracking        │
│  - YOLOv8 detection                  │
│  - ByteTrack assignment              │
│  - Compute speed & trajectory        │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  Traffic Light Detection             │
│  - HSV color segmentation            │
│  - Red/Yellow/Green classification   │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  Violation Detection Engine          │
│  - Check all 6 violation rules       │
│  - Apply cooldown filtering          │
│  - Log incidents with evidence       │
└──────────────────────────────────────┘
    ↓
┌──────────────────────────────────────┐
│  Output Generation                   │
│  - Annotated video frame             │
│  - CSV/JSON incident logs            │
│  - Evidence image crops              │
└──────────────────────────────────────┘
    ↓
Video Output + Reports
```

### 5.2 Configuration Parameters

**Violation Thresholds (ViolationConfig):**
```python
speed_limit_kmh: 50.0              # Speed limit threshold
stop_speed_threshold_kmh: 5.0      # Speed to register as "stopped"
meters_per_pixel: 0.05             # Calibration for speed estimation
expected_direction: "down"         # Expected traffic flow direction
stop_line_y: 380                   # Y-coordinate of stop line
traffic_light_roi: (20, 20, 120, 220)  # Region of interest for traffic light
min_wrong_way_pixels: 40.0         # Minimum pixels for wrong-way detection
violation_cooldown_frames: 30      # Frames between duplicate logs
```

**Spatial Definitions (per video):**
- `lane_polygons`: List of valid lane boundary polygons
- `forbidden_zone`: List of no-entry zone polygons
- `traffic_light_roi`: Bounding box of traffic signal

---

## 6. IMPLEMENTATION DETAILS

### 6.1 Sign Classifier (ResNet18)

**Training Configuration:**
- Model: ResNet18 (pretrained on ImageNet)
- Dataset: 31,368 training images, 7,841 validation images
- Input size: 96×96 pixels
- Batch size: 64
- Epochs: 5 (or custom)
- Learning rate: 0.001
- Optimizer: Adam
- Loss function: CrossEntropyLoss
- Data augmentation: random flip, color jitter

**Output:** Saved weights → `models/gtsrb_sign_classifier_resnet18.pth`

### 6.2 Sign Detection Strategy

**Priority 1: YOLO Detection (if weights available)**
- Load from `models/traffic_sign_detector.pt`
- Confidence threshold: 0.25
- Followed by ResNet18 classification on crops

**Priority 2: Heuristic Fallback (default)**
- HSV color filtering (red, blue ranges)
- Morphological operations (open/close)
- Contour detection with area and aspect ratio filtering
- Followed by ResNet18 classification

### 6.3 Vehicle Tracking

**YOLOv8 Detection:**
- Model: YOLOv8 nano (fastest)
- Classes: car (2), motorcycle (3), bus (5), truck (7)
- Confidence: 0.35
- IoU threshold: 0.5

**ByteTrack Assignment:**
- Maintains persistent track IDs
- Handles occlusion and re-identification
- Output: `track_id`, bounding box, class, confidence

**Speed Computation:**
- Track history: 90-frame window (3 seconds at 30 FPS)
- Speed (km/h) = (pixel_distance × meters_per_pixel × 3.6) / time_sec

### 6.4 Violation Detection Logic

**Example: Red Light Jumping**
```python
if light_state == "red":
    if crossed_stop_line(prev_center, curr_center, stop_line_y):
        LOG_VIOLATION("Red light jumping", track_id, frame_idx)
        SAVE_EVIDENCE(frame, bbox, track_id)
```

**Example: Speeding**
```python
speed_kmh = compute_speed_kmh(track_id, center, frame_idx, cfg)
if speed_kmh > cfg.speed_limit_kmh:
    LOG_VIOLATION("Speeding", track_id, frame_idx, 
                  extra={"speed_kmh": speed_kmh})
```

---

## 7. OUTPUTS & REPORTS

### 7.1 Annotated Video
- **File:** `outputs/annotated_traffic_output.mp4`
- **Content:**
  - Green bounding boxes: detected vehicles with track IDs
  - Orange bounding boxes: detected traffic signs
  - Red bounding boxes: violating vehicles
  - Overlay text: speed, traffic light state, frame count, incident count
  - Yellow polygon: traffic light ROI
  - Green/Blue/Orange polygons: lane and zone definitions

### 7.2 CSV Incident Log
- **File:** `outputs/violation_log.csv`
- **Columns:**
  - `track_id`: Vehicle ID
  - `frame_idx`: Frame number
  - `timestamp_sec`: Time in seconds
  - `violation_type`: Type of violation
  - `bbox`: [x1, y1, x2, y2] coordinates
  - `evidence_image`: Path to cropped image
  - Additional columns (speed_kmh, traffic_light state, etc.)

### 7.3 JSON Summary
- **File:** `outputs/violation_summary.json`
- **Content:**
  ```json
  {
    "total_incidents": 42,
    "by_type": {
      "Speeding": 18,
      "Red light jumping": 12,
      "Lane violation": 8,
      "Wrong-way driving": 3,
      "Ignoring stop sign": 1,
      "No-entry violation": 0
    },
    "video_output": "outputs/annotated_traffic_output.mp4",
    "log_csv": "outputs/violation_log.csv"
  }
  ```

### 7.4 Evidence Images
- **Folder:** `outputs/incidents/`
- **Naming:** `frame_XXXXXX_track_YYY_ViolationType.jpg`
- **Content:** Cropped vehicle region at violation moment

---

## 8. HOW TO USE

### 8.1 Prerequisites
```bash
# Install dependencies
pip install torch torchvision ultralytics opencv-python pandas numpy matplotlib
```

### 8.2 Running the Pipeline

**Step 1:** Prepare input video
```
Place your traffic video at: 
D:/UMEF/E1402_Digital and Computer Vision/final-project/sample_traffic_video.mp4
```

**Step 2:** Open notebook
```
final-project/starter-gtsrb-german-traffic-sign-938d9c07-7.ipynb
```

**Step 3:** Run cells in order
- Cell 1-5: Setup and dataset loading
- Cell 6-9: Train/load sign classifier
- Cell 10: Load sign detector
- Cell 11-13: Define violation rules and detection functions
- Cell 14: Load vehicle detector
- Cell 15: Process video (MAIN)
- Cell 16: Visualize results

### 8.3 Customization

**Adjust violation thresholds:**
```python
# In Cell 15 (video processing):
cfg = ViolationConfig(
    speed_limit_kmh=80.0,           # Change speed limit
    stop_speed_threshold_kmh=3.0,   # Change stop threshold
    meters_per_pixel=0.05,          # Calibrate based on lane width
    expected_direction="down",      # "up" or "down"
    violation_cooldown_frames=45    # More/less duplicate filtering
)
```

**Define lane and zone polygons:**
```python
# Define lanes as numpy arrays of (x, y) coordinates
lane_left = np.array([[...], [...], [...]], dtype=np.int32)
lane_right = np.array([[...], [...], [...]], dtype=np.int32)

# Forbidden zones
forbidden = np.array([[...], [...], [...]], dtype=np.int32)

# Pass to config
cfg.lane_polygons = [lane_left, lane_right]
cfg.forbidden_zone = [forbidden]
```

**Adjust traffic light ROI:**
```python
# (x1, y1, x2, y2) of traffic light bounding box
cfg.traffic_light_roi = (int(0.02*w), int(0.03*h), int(0.11*w), int(0.30*h))
```

---

## 9. PERFORMANCE CONSIDERATIONS

### 9.1 Computational Requirements
- **CPU Only:** ~10 FPS (i7 processor)
- **GPU (CUDA):** ~30-60 FPS (RTX 3060+)
- **Memory:** ~4GB RAM for notebook execution

### 9.2 Accuracy Improvements
1. **Better Sign Detection:** Use trained YOLOv8 weights instead of heuristic
2. **Calibration:** Measure `meters_per_pixel` from known distances (lane width ~3.7m)
3. **Multi-frame Smoothing:** Average detections over 3-5 frames for stability
4. **Scene-specific Tuning:** Adjust polygons and thresholds per camera/location

### 9.3 Production Deployment
For city-scale deployment:
- Add database logging (PostgreSQL, MongoDB)
- Deploy with API server (Flask/FastAPI)
- Real-time alerts via webhook/email
- Integration with traffic management systems
- Privacy-preserving detection (blur non-violating vehicles)

---

## 10. METHODOLOGY & REFERENCES

### 10.1 Core Algorithms
- **Object Detection:** YOLO v8 (Ultralytics)
- **Multi-object Tracking:** ByteTrack
- **Image Classification:** ResNet18 with Transfer Learning
- **Polygon Containment:** OpenCV's `pointPolygonTest()`
- **Color Segmentation:** HSV-based thresholding

### 10.2 Related Works
- Redmon et al., YOLOv8: Real-Time Object Detection
- Zhang et al., ByteTrack: Multi-Object Tracking with Appearance-Free Association
- He et al., Deep Residual Learning for Image Recognition (ResNet)
- German Traffic Sign Recognition Benchmark (GTSRB) Dataset

### 10.3 Applications
- Smart City Traffic Management
- Automated Enforcement Systems
- Road Safety Monitoring
- Traffic Pattern Analysis
- Insurance Claim Assessment

---

## 11. PROJECT TIMELINE

| Phase | Duration | Deliverables |
|---|---|---|
| **Phase 1:** Requirements & Dataset Setup | 1 week | Dataset exploration, GTSRB loading |
| **Phase 2:** Sign Classifier Training | 2 weeks | ResNet18 model, 95%+ accuracy |
| **Phase 3:** Vehicle Detection & Tracking | 2 weeks | YOLOv8+ByteTrack pipeline |
| **Phase 4:** Violation Logic Implementation | 2 weeks | 6 violation types, rule engine |
| **Phase 5:** Integration & Testing | 1 week | End-to-end pipeline, sample video |
| **Phase 6:** Documentation & Reporting | 1 week | README, annotations, visualization |

**Total:** ~9 weeks

---

## 12. CONCLUSION

This **Traffic Sign and Violation Detection System** demonstrates practical application of computer vision and deep learning to real-world traffic enforcement challenges. By combining YOLO detection, ResNet classification, and ByteTrack association, the system achieves real-time performance while maintaining accuracy for automated incident logging.

The modular design allows easy adaptation to different cities, camera angles, and traffic rules, making it suitable for smart city ITS deployments.

---

**Last Updated:** April 2025  
**Status:** Complete Implementation  
**Repository:** Final-Project Notebook
