# MIRA — 3D Character Animation & Digital Human Asset Pipeline

**Canonical Identity Anchor:** `MIRA_FACE_MODEL` (`v1`)  
**Product:** MIRA (Medical Intelligent Response Assistant)  
**Specification Level:** Block 3 — Interactive Character Animation Foundation  
**Target Output:** High-Fidelity Realistic 3D Digital Human (glTF / Three.js / WebGPU)

---

## 1. Executive Summary & Asset Evaluation

### Current Asset Baseline (Block 2 & 3)
- **Format:** Single flattened raster image (`PNG`, 1536 × 1024 px, 2.63 MB).
- **File Path:** `assets/mira/identity/MIRA_FACE_MODEL.png` (and root `MIRA_FACE_MODEL.png`).
- **Integrity Checksum:** `bf3b7cdc290d28ca7500b3d55679cbd98a397b4ec873dd86e8c910c46d1b44dc`.
- **Classification:** **Flattened 2D Image Asset** (Option 1).
- **Current Limitation:** A flattened 2D asset lacks independent mesh topology, depth planes, and skeletal bones. True 3-axis ocular rotation, full eyelid roll, jaw articulation across phonemes, and 3D head pitch/yaw cannot be achieved from a flat 2D image without warping or distortion.
- **Architectural Solution:** Rather than applying artificial, cartoonish 2D image distortions (bouncing, zooming, glowing pulses), Block 3 establishes the complete, production-grade **Character State & Animation Engine** (`MiraAnimationController`, `MiraEyeController`, `MiraAttentionController`, `MiraLipSyncController`, `MiraExpressionController`) designed to seamlessly drive both our calibrated 2.5D presentation fallback and the forthcoming **3D Digital Human Engine**.

---

## 2. Evaluation of Animation Pathways

### Option A: 2D / 2.5D Character Animation (Rive / Spine / Cutout)
- **Strengths:** Lightweight, simple vector format.
- **Critical Flaws for MIRA:**
  - Inevitably produces a stylized, illustrated, or "explainer video" cartoon aesthetic.
  - Incapable of authentic depth parallax during gaze orientation and head movement.
  - Fails the core requirement: *"MIRA should NOT look like: a cartoon, a game NPC, a generic AI hologram, a robotic assistant, an anime character."*
  - **Verdict:** REJECTED as the primary long-term technology.

### Option B: 3D Digital Human (Blender + FACS Rigging + Three.js / WebGPU)
- **Strengths:**
  - Full physiological realism for medical bedside interaction.
  - Photorealistic PBR rendering with subsurface scattering for warm South Indian skin tones.
  - Support for 52 standard ARKit/FACS blendshapes for natural micro-expressions.
  - Ocular parallax with separate cornea, iris, pupil, and sclera meshes.
  - Viseme-accurate phonetic speech synchronization.
  - 3-axis head and neck rotational degrees of freedom (pitch, yaw, roll).
  - **Verdict:** **SELECTED as Canonical Architecture.**

---

## 3. End-to-End Asset Transformation Pipeline

```
  MIRA_FACE_MODEL_v1 (Canonical PNG Anchor)
                   │
                   ▼ [Phase 1: Photogrammetric Reconstruction]
      High-Res 3D Head Mesh (ZBrush / Blender)
                   │
                   ▼ [Phase 2: Topology & Retopology]
    Production Topology (Quad-based, ~25,000 polys)
                   │
                   ▼ [Phase 3: Skeletal & FACS Rigging]
   52 FACS Blendshapes + Cranial / Ocular Bone Hierarchy
                   │
                   ▼ [Phase 4: PBR Texture Baking]
  4K Albedo, Normal, Roughness, Subsurface Scattering (SSS)
                   │
                   ▼ [Phase 5: Hair & Uniform Groom]
 Clinical Low Bun Hair Cards + Tailored Medical Lab Coat
                   │
                   ▼ [Phase 6: Real-Time Optimization]
 glTF 2.0 / GLB Container (Draco compression, KHR_materials)
                   │
                   ▼ [Phase 7: Web Runtime Integration]
  Three.js / WebGPU Driven by MiraAnimationController
```

---

## 4. Rigging & Blendshape Specification

### Facial Action Coding System (FACS) Blendshapes
The 3D model must implement the standard 52 ARKit-compatible FACS blendshapes to interface directly with `MiraExpressionController` and `MiraLipSyncController`:

| Category | Morph Target Names | Clinical Function in MIRA |
| :--- | :--- | :--- |
| **Brows** | `browDownLeft`, `browDownRight`, `browInnerUp`, `browOuterUpLeft`, `browOuterUpRight` | Empathetic listening, clinical concern, reassurance |
| **Eyes** | `eyeBlinkLeft`, `eyeBlinkRight`, `eyeSquintLeft`, `eyeSquintRight`, `eyeWideLeft`, `eyeWideRight` | Organic blinking (160ms cycle), focused attention, alert vigilance |
| **Gaze** | `eyeLookDownLeft`, `eyeLookInLeft`, `eyeLookOutLeft`, `eyeLookUpLeft`, ... | Saccades, looking at user (0,0), looking at vitals monitor |
| **Cheeks** | `cheekPuff`, `cheekSquintLeft`, `cheekSquintRight` | Warm clinical smile, bedside comfort |
| **Jaw & Mouth** | `jawOpen`, `jawForward`, `jawLeft`, `jawRight` | Syllabic openness during speaking |
| **Lips** | `mouthFunnel`, `mouthPucker`, `mouthSmileLeft`, `mouthSmileRight`, `mouthFrownLeft`, `mouthFrownRight`, `mouthDimpleLeft`, `mouthDimpleRight`, `mouthStretchLeft`, `mouthStretchRight`, `mouthRollLower`, `mouthRollUpper`, `mouthShrugLower`, `mouthShrugUpper`, `mouthPressLeft`, `mouthPressRight`, `mouthLowerDownLeft`, `mouthLowerDownRight`, `mouthUpperUpLeft`, `mouthUpperUpRight` | Visemes: `AA`, `E`, `I`, `O`, `U`, `PP`, `FF`, `TH`, `DD`, `KK`, `CH`, `SS`, `NN`, `RR` |

---

## 5. Physical Material & PBR Specifications

To preserve the warm, professional South Indian clinical identity:

- **Albedo / Base Color:** Warm golden olive undertone matching `MIRA_FACE_MODEL_v1` RGB values sampled from cheeks, jaw, and forehead.
- **Subsurface Scattering (SSS):** Multi-layer skin shader profile:
  - Epidermis depth: ~1.2 mm
  - Subdermal hemoglobin scattering radius: `(0.48, 0.16, 0.11)`
  - Soft matte finish (specular roughness 0.42 - 0.58) preventing synthetic "plastic" or "doll-like" sheen.
- **Eyes:**
  - Separate transparent Cornea mesh with Fresnel index of refraction (IOR 1.376).
  - Deep dark espresso brown iris texture with realistic trabecular radial fibrous detail.
  - Pupil dilation target (0.8x to 1.2x) modulated by ambient light and clinical focus.
- **Hair:**
  - Natural deep brown/black tone `#1C130E`.
  - Clean parting with gentle clinical low bun, zero decorative accessories.
- **Attire:**
  - Crisp clinical white lab coat (`#FFFFFF`) with tailored lapels and stethoscope/diagnostic badge.

---

## 6. Runtime Integration Architecture

The Python and JavaScript `MiraAnimationController` implementations provide the exact stream of parameters consumed by the 3D renderer:

```typescript
// Example Three.js render hook consuming MiraAnimationController telemetry:
function onMiraFrame(frameState: CharacterFrameState, miraMesh: THREE.SkinnedMesh) {
  const morphs = miraMesh.morphTargetInfluences;
  const dict = miraMesh.morphTargetDictionary;

  // 1. Eyelid Occlusion
  morphs[dict['eyeBlinkLeft']] = frameState.eye_state.blink_weight;
  morphs[dict['eyeBlinkRight']] = frameState.eye_state.blink_weight;

  // 2. Gaze Parallax
  leftEyeBone.rotation.y = THREE.MathUtils.degToRad(frameState.eye_state.yaw_deg);
  leftEyeBone.rotation.x = THREE.MathUtils.degToRad(frameState.eye_state.pitch_deg);

  // 3. Head & Attention Orientation
  headBone.rotation.x = THREE.MathUtils.degToRad(frameState.attention_state.head_pitch_deg);
  headBone.rotation.y = THREE.MathUtils.degToRad(frameState.attention_state.head_yaw_deg);
  headBone.rotation.z = THREE.MathUtils.degToRad(frameState.attention_state.head_roll_deg);

  // 4. Clinical Facial Expression
  morphs[dict['browInnerUp']] = frameState.expression_weights.brow_inner_up;
  morphs[dict['browDownLeft']] = frameState.expression_weights.brow_down_concern;
  morphs[dict['mouthSmileLeft']] = frameState.expression_weights.mouth_smile_warmth;

  // 5. Phonetic Lip-Sync
  morphs[dict['jawOpen']] = frameState.mouth_weights.jaw_open;
  morphs[dict['mouthPucker']] = frameState.mouth_weights.lip_pucker;
  morphs[dict['mouthFunnel']] = frameState.mouth_weights.lip_funnel;
}
```

---

## 7. Versioning and Integrity Safeguards

- Canonical anchor file `assets/mira/identity/MIRA_FACE_MODEL.png` is permanently write-protected and version-locked as `MIRA_FACE_MODEL_v1`.
- Any derived 3D mesh must pass cryptographic hashing and identity audit approval before deployment to `assets/mira/character/MIRA_3D_MODEL_v1.glb`.
- Automated test suites verify asset checksums on every build.
