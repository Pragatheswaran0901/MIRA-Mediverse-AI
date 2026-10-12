/**
 * MIRA Interactive Character Animation System (Block 3)
 * 
 * Canonical Identity Reference: MIRA_FACE_MODEL (v1)
 * Purpose: Deliver subtle, healthcare-appropriate interactive digital human presentation:
 * - MiraAnimationController: State-driven priority engine & conversational lifecycle
 * - MiraEyeController: Organic blinking, micro-saccades & gaze targets
 * - MiraAttentionController: Head orientation, clinical respiratory rhythm & attentive nods
 * - MiraExpressionController: 10 clinical facial expressions with subtle morphing
 * - MiraLipSyncController: Viseme mapping & speech cadence mouth articulation
 * - MiraEventBus: Decoupled pub/sub event integration
 * - Performance: Lifecycle-aware, requestAnimationFrame loop, IntersectionObserver pause
 * 
 * STRICT MANDATES:
 * - Canonical identity preserved without facial redesign or distortion
 * - NO continuous zoom, NO bouncing, NO full-character rotation, NO fake glowing pulses
 * - Healthcare bedside presence: calm, subtle, professional, empathetic
 * - Absolutely NO AI logic, LLM calls, or clinical reasoning contained herein
 */

(function () {
  'use strict';

  // ============================================================================
  // Canonical Constants & Priority Registry
  // ============================================================================

  const STATE_PRIORITIES = {
    EMERGENCY: 100,
    ESCALATING: 90,
    SERIOUS: 80,
    CONCERNED: 70,
    SPEAKING: 60,
    LISTENING: 50,
    THINKING: 45,
    GREETING: 40,
    REASSURING: 30,
    CALMING: 30,
    FRIENDLY: 30,
    COMPLETED: 20,
    IDLE: 10,
  };

  const MIRA_STATES = {
    IDLE: {
      name: "Bedside Idle",
      intent: "Observing bedside and ready to assist",
      accent: "#0D9488",
      expression: "NEUTRAL",
      gaze: "USER",
      breathingCpm: 14.0,
      blinkInterval: 3.8,
      lean: 0.0,
      tilt: 0.0,
    },
    GREETING: {
      name: "Warm Greeting",
      intent: "Welcoming patient with clinical warmth",
      accent: "#F472B6",
      expression: "HAPPY",
      gaze: "USER",
      breathingCpm: 15.0,
      blinkInterval: 3.2,
      lean: 0.15,
      tilt: 1.5,
    },
    LISTENING: {
      name: "Active Listening",
      intent: "Attentively capturing patient symptoms",
      accent: "#3B82F6",
      expression: "ATTENTIVE",
      gaze: "USER",
      breathingCpm: 13.0,
      blinkInterval: 4.0,
      lean: 0.35,
      tilt: 1.0,
    },
    THINKING: {
      name: "Clinical Reasoning",
      intent: "Synthesizing clinical criteria and protocols",
      accent: "#8B5CF6",
      expression: "THINKING",
      gaze: "AWAY",
      breathingCpm: 12.0,
      blinkInterval: 4.5,
      lean: 0.0,
      tilt: -1.5,
    },
    SPEAKING: {
      name: "Clinical Delivery",
      intent: "Delivering clear, accessible medical advice",
      accent: "#0EA5E9",
      expression: "ATTENTIVE",
      gaze: "USER",
      breathingCpm: 16.0,
      blinkInterval: 3.0,
      lean: 0.1,
      tilt: 0.5,
    },
    FRIENDLY: {
      name: "Companion Friendly",
      intent: "Alleviating healthcare anxiety and isolation",
      accent: "#EC4899",
      expression: "HAPPY",
      gaze: "USER",
      breathingCpm: 14.0,
      blinkInterval: 3.5,
      lean: 0.1,
      tilt: 2.0,
    },
    CONCERNED: {
      name: "Clinical Concern",
      intent: "Vigilant scrutiny of symptom developments",
      accent: "#F59E0B",
      expression: "CONCERNED",
      gaze: "USER",
      breathingCpm: 16.0,
      blinkInterval: 3.0,
      lean: 0.25,
      tilt: 1.0,
    },
    SERIOUS: {
      name: "Firm Directive",
      intent: "Delivering urgent medical instructions",
      accent: "#EA580C",
      expression: "SERIOUS",
      gaze: "USER",
      breathingCpm: 18.0,
      blinkInterval: 4.8,
      lean: 0.0,
      tilt: 0.0,
    },
    REASSURING: {
      name: "Reassurance",
      intent: "Comforting patient with empathetic reassurance",
      accent: "#E2C799",
      expression: "REASSURING",
      gaze: "USER",
      breathingCpm: 12.0,
      blinkInterval: 3.4,
      lean: 0.15,
      tilt: 1.8,
    },
    EMERGENCY: {
      name: "Emergency Escalation",
      intent: "Acute crisis: direct patient to 911 / emergency services",
      accent: "#DC2626",
      expression: "EMERGENCY",
      gaze: "USER",
      breathingCpm: 20.0,
      blinkInterval: 5.0,
      lean: 0.0,
      tilt: 0.0,
    },
    ESCALATING: {
      name: "Triage Escalating",
      intent: "Transitioning severity to elevated clinical tier",
      accent: "#D97706",
      expression: "CONCERNED",
      gaze: "USER",
      breathingCpm: 17.0,
      blinkInterval: 3.2,
      lean: 0.2,
      tilt: 0.5,
    },
    CALMING: {
      name: "Paced Calming",
      intent: "Guiding patient through paced respiratory calming",
      accent: "#14B8A6",
      expression: "CALM",
      gaze: "USER",
      breathingCpm: 8.0,
      blinkInterval: 4.2,
      lean: 0.05,
      tilt: 0.5,
    },
    COMPLETED: {
      name: "Session Completed",
      intent: "Satisfied consultation closure and care confirmation",
      accent: "#10B981",
      expression: "CALM",
      gaze: "USER",
      breathingCpm: 14.0,
      blinkInterval: 3.6,
      lean: 0.0,
      tilt: 1.0,
    },
  };

  const CANONICAL_ASSET_URL = "/assets/mira/identity/MIRA_FACE_MODEL.png";
  const FALLBACK_ASSET_URL = "/MIRA_FACE_MODEL.png";

  // ============================================================================
  // Event Bus (Decoupled Pub/Sub)
  // ============================================================================

  class MiraEventBus {
    constructor() {
      this._subscribers = new Map();
      this._wildcard = [];
    }

    subscribe(eventType, callback) {
      if (!this._subscribers.has(eventType)) {
        this._subscribers.set(eventType, []);
      }
      this._subscribers.get(eventType).push(callback);
      return () => {
        const list = this._subscribers.get(eventType);
        if (list) {
          const idx = list.indexOf(callback);
          if (idx !== -1) list.splice(idx, 1);
        }
      };
    }

    subscribeAll(callback) {
      this._wildcard.push(callback);
      return () => {
        const idx = this._wildcard.indexOf(callback);
        if (idx !== -1) this._wildcard.splice(idx, 1);
      };
    }

    publish(eventType, metadata = {}) {
      const payload = {
        event: eventType,
        timestamp: Date.now(),
        metadata,
      };
      const list = this._subscribers.get(eventType) || [];
      list.forEach((cb) => {
        try { cb(payload); } catch (e) { console.error(e); }
      });
      this._wildcard.forEach((cb) => {
        try { cb(payload); } catch (e) { console.error(e); }
      });
      return payload;
    }
  }

  // ============================================================================
  // Eye Subsystem Controller
  // ============================================================================

  const GAZE_COORDINATES = {
    USER: { yaw: 0.0, pitch: 0.0 },
    SCREEN: { yaw: -2.8, pitch: -1.2 },
    LEFT: { yaw: -3.5, pitch: 0.0 },
    RIGHT: { yaw: 3.5, pitch: 0.0 },
    UP: { yaw: 0.0, pitch: 2.2 },
    DOWN: { yaw: 0.0, pitch: -2.0 },
    AWAY: { yaw: 2.6, pitch: 1.4 },
    CENTER: { yaw: 0.0, pitch: 0.0 },
  };

  class MiraEyeController {
    constructor(baseBlinkInterval = 3.8) {
      this.target = "USER";
      this.currentYaw = 0.0;
      this.currentPitch = 0.0;
      this.targetYaw = 0.0;
      this.targetPitch = 0.0;

      this.baseBlinkInterval = baseBlinkInterval;
      this.timeUntilBlink = this._computeNextBlinkInterval();
      this.isBlinking = false;
      this.blinkElapsedSec = 0.0;
      this.blinkDurationSec = 0.16; // 160ms biological blink
      this.blinkWeight = 0.0;

      this.saccadeTimer = 0.0;
      this.saccadeInterval = 1.8;
      this.saccadeX = 0.0;
      this.saccadeY = 0.0;
      this.squintWeight = 0.0;
    }

    _computeNextBlinkInterval() {
      const jitter = (Math.random() - 0.5) * 1.6;
      return Math.max(2.0, this.baseBlinkInterval + jitter);
    }

    lookAt(targetKey) {
      const upper = (targetKey || "USER").toUpperCase();
      this.target = GAZE_COORDINATES[upper] ? upper : "USER";
      const coords = GAZE_COORDINATES[this.target];
      this.targetYaw = coords.yaw;
      this.targetPitch = coords.pitch;
    }

    lookAtUser() { this.lookAt("USER"); }
    lookAtScreen() { this.lookAt("SCREEN"); }
    lookAway() { this.lookAt("AWAY"); }

    blink() {
      if (!this.isBlinking) {
        this.isBlinking = true;
        this.blinkElapsedSec = 0.0;
        this.blinkWeight = 0.0;
      }
    }

    update(dt) {
      // 1. Blinking Cycle
      if (this.isBlinking) {
        this.blinkElapsedSec += dt;
        const progress = this.blinkElapsedSec / this.blinkDurationSec;
        if (progress >= 1.0) {
          this.isBlinking = false;
          this.blinkWeight = 0.0;
          this.timeUntilBlink = this._computeNextBlinkInterval();
        } else {
          // Fast closing 35%, gentle opening 65%
          if (progress < 0.35) {
            this.blinkWeight = Math.sin((progress / 0.35) * (Math.PI / 2.0));
          } else {
            const openProg = (progress - 0.35) / 0.65;
            this.blinkWeight = Math.cos(openProg * (Math.PI / 2.0));
          }
          this.blinkWeight = Math.max(0.0, Math.min(1.0, this.blinkWeight));
        }
      } else {
        this.timeUntilBlink -= dt;
        if (this.timeUntilBlink <= 0.0) {
          this.blink();
        }
      }

      // 2. Smooth Gaze Damping
      const gazeSpeed = Math.min(1.0, 7.0 * dt);
      this.currentYaw += (this.targetYaw - this.currentYaw) * gazeSpeed;
      this.currentPitch += (this.targetPitch - this.currentPitch) * gazeSpeed;

      // 3. Subtle Micro-Saccades
      this.saccadeTimer += dt;
      if (this.saccadeTimer >= this.saccadeInterval) {
        this.saccadeTimer = 0.0;
        this.saccadeInterval = 1.2 + Math.random() * 1.4;
        this.saccadeX = (Math.random() - 0.5) * 0.6;
        this.saccadeY = (Math.random() - 0.5) * 0.4;
      }

      return {
        target: this.target,
        yaw: this.currentYaw + this.saccadeX,
        pitch: this.currentPitch + this.saccadeY,
        blinkWeight: this.blinkWeight,
        isBlinking: this.isBlinking,
        squintWeight: this.squintWeight,
      };
    }

    reset() {
      this.lookAtUser();
      this.currentYaw = 0.0;
      this.currentPitch = 0.0;
      this.isBlinking = false;
      this.blinkWeight = 0.0;
      this.squintWeight = 0.0;
      this.saccadeX = 0.0;
      this.saccadeY = 0.0;
      this.timeUntilBlink = this._computeNextBlinkInterval();
    }
  }

  // ============================================================================
  // Attention & Head Subsystem Controller
  // ============================================================================

  const ATTENTION_TARGETS = {
    USER: { yaw: 0.0, pitch: 0.0, roll: 0.0 },
    SCREEN: { yaw: -1.8, pitch: -0.8, roll: 0.0 },
    LEFT: { yaw: -2.5, pitch: 0.0, roll: -0.5 },
    RIGHT: { yaw: 2.5, pitch: 0.0, roll: 0.5 },
    UP: { yaw: 0.0, pitch: 1.5, roll: 0.2 },
    DOWN: { yaw: 0.0, pitch: -1.5, roll: 0.0 },
    CENTER: { yaw: 0.0, pitch: 0.0, roll: 0.0 },
  };

  class MiraAttentionController {
    constructor(breathingRateCpm = 14.0) {
      this.target = "USER";
      this.currentYaw = 0.0;
      this.currentPitch = 0.0;
      this.currentRoll = 0.0;
      this.targetYaw = 0.0;
      this.targetPitch = 0.0;
      this.targetRoll = 0.0;

      this.postureLean = 0.0;
      this.targetPostureLean = 0.0;

      this.breathingRateCpm = breathingRateCpm;
      this.breathingPhase = 0.0;

      this.isNodding = false;
      this.nodElapsedSec = 0.0;
      this.nodDurationSec = 1.1;
      this.nodAmplitudeDeg = 1.8;
      this.nodOffsetPitch = 0.0;
    }

    setTarget(targetKey) {
      const upper = (targetKey || "USER").toUpperCase();
      this.target = ATTENTION_TARGETS[upper] ? upper : "USER";
      const coords = ATTENTION_TARGETS[this.target];
      this.targetYaw = coords.yaw;
      this.targetPitch = coords.pitch;
      this.targetRoll = coords.roll;
    }

    orientToUser() { this.setTarget("USER"); }
    orientToScreen() { this.setTarget("SCREEN"); }

    triggerListeningNod() {
      if (!this.isNodding) {
        this.isNodding = true;
        this.nodElapsedSec = 0.0;
        this.nodOffsetPitch = 0.0;
      }
    }

    update(dt) {
      // 1. Subtle Clinical Respiratory Rhythm (14 CPM = 0.233 Hz)
      const freqHz = this.breathingRateCpm / 60.0;
      this.breathingPhase += dt * freqHz * 2.0 * Math.PI;
      if (this.breathingPhase > 2.0 * Math.PI) {
        this.breathingPhase -= 2.0 * Math.PI;
      }
      const breatheSin = Math.sin(this.breathingPhase);
      const breathingOffsetY = breatheSin * 0.8; // Max 0.8px vertical motion
      const breathingScale = 1.0 + (breatheSin * 0.0015); // Max 0.15% scale shift

      // 2. Attentive Listening Nod
      if (this.isNodding) {
        this.nodElapsedSec += dt;
        const progress = this.nodElapsedSec / this.nodDurationSec;
        if (progress >= 1.0) {
          this.isNodding = false;
          this.nodOffsetPitch = 0.0;
        } else {
          this.nodOffsetPitch = -Math.sin(progress * Math.PI) * this.nodAmplitudeDeg;
        }
      } else {
        this.nodOffsetPitch = 0.0;
      }

      // 3. Head & Posture Smoothing
      const speed = Math.min(1.0, 3.5 * dt);
      this.currentYaw += (this.targetYaw - this.currentYaw) * speed;
      this.currentPitch += (this.targetPitch - this.currentPitch) * speed;
      this.currentRoll += (this.targetRoll - this.currentRoll) * speed;
      this.postureLean += (this.targetPostureLean - this.postureLean) * speed;

      return {
        target: this.target,
        yaw: this.currentYaw,
        pitch: this.currentPitch + this.nodOffsetPitch,
        roll: this.currentRoll,
        lean: this.postureLean,
        breathingOffsetY,
        breathingScale,
        isNodding: this.isNodding,
      };
    }

    reset() {
      this.orientToUser();
      this.currentYaw = 0.0;
      this.currentPitch = 0.0;
      this.currentRoll = 0.0;
      this.postureLean = 0.0;
      this.targetPostureLean = 0.0;
      this.isNodding = false;
      this.nodOffsetPitch = 0.0;
    }
  }

  // ============================================================================
  // Lip Sync Subsystem Controller
  // ============================================================================

  const VISEME_WEIGHTS = {
    SIL: { jaw: 0.0, pucker: 0.0, wide: 0.0 },
    PP:  { jaw: 0.05, pucker: 0.0, wide: 0.0 },
    FF:  { jaw: 0.15, pucker: 0.0, wide: 0.1 },
    TH:  { jaw: 0.2,  pucker: 0.0, wide: 0.2 },
    DD:  { jaw: 0.25, pucker: 0.0, wide: 0.25 },
    KK:  { jaw: 0.3,  pucker: 0.0, wide: 0.2 },
    CH:  { jaw: 0.25, pucker: 0.2, wide: 0.1 },
    SS:  { jaw: 0.15, pucker: 0.0, wide: 0.3 },
    NN:  { jaw: 0.2,  pucker: 0.0, wide: 0.2 },
    RR:  { jaw: 0.25, pucker: 0.3, wide: 0.0 },
    AA:  { jaw: 0.65, pucker: 0.0, wide: 0.2 },
    E:   { jaw: 0.4,  pucker: 0.0, wide: 0.4 },
    I:   { jaw: 0.25, pucker: 0.0, wide: 0.45 },
    O:   { jaw: 0.5,  pucker: 0.4, wide: 0.0 },
    U:   { jaw: 0.3,  pucker: 0.6, wide: 0.0 },
  };

  class MiraLipSyncController {
    constructor() {
      this.isActive = false;
      this.currentViseme = "SIL";
      this.jawOpen = 0.0;
      this.lipPucker = 0.0;
      this.lipWide = 0.0;
      this.targetJaw = 0.0;
      this.targetPucker = 0.0;
      this.targetWide = 0.0;

      this.speechCadencePhase = 0.0;
      this.cadenceRateHz = 3.2; // ~150 WPM syllable rhythm
    }

    feedViseme(visemeKey, weight = 1.0) {
      const v = (visemeKey || "SIL").toUpperCase();
      this.currentViseme = VISEME_WEIGHTS[v] ? v : "SIL";
      this.isActive = (this.currentViseme !== "SIL");
      const base = VISEME_WEIGHTS[this.currentViseme];
      const w = Math.max(0.0, Math.min(1.0, weight));
      this.targetJaw = base.jaw * w;
      this.targetPucker = base.pucker * w;
      this.targetWide = base.wide * w;
    }

    feedAudioEnergy(rms, cadenceWpm = 150) {
      const energy = Math.max(0.0, Math.min(1.0, rms));
      if (energy <= 0.05) {
        this.stop();
        return;
      }
      this.isActive = true;
      this.targetJaw = Math.min(0.65, energy * 0.85);
      this.targetWide = energy * 0.3;
      this.targetPucker = 0.0;
      this.currentViseme = (this.targetJaw > 0.3) ? "AA" : "E";
    }

    startSpeakingCadence() {
      this.isActive = true;
    }

    stop() {
      this.isActive = false;
      this.currentViseme = "SIL";
      this.targetJaw = 0.0;
      this.targetPucker = 0.0;
      this.targetWide = 0.0;
    }

    update(dt) {
      if (this.isActive && this.targetJaw === 0.0) {
        // Natural speech syllabic cadence modulation if no specific viseme passed
        this.speechCadencePhase += dt * this.cadenceRateHz * 2.0 * Math.PI;
        const syl = Math.max(0.0, Math.sin(this.speechCadencePhase));
        this.targetJaw = syl * 0.4;
        this.targetWide = syl * 0.2;
      }

      // Smooth mouth damping
      const speed = Math.min(1.0, 16.0 * dt);
      this.jawOpen += (this.targetJaw - this.jawOpen) * speed;
      this.lipPucker += (this.targetPucker - this.lipPucker) * speed;
      this.lipWide += (this.targetWide - this.lipWide) * speed;

      return {
        isActive: this.isActive,
        viseme: this.currentViseme,
        jawOpen: this.jawOpen,
        lipPucker: this.lipPucker,
        lipWide: this.lipWide,
      };
    }
  }

  // ============================================================================
  // Central Character Animation Controller
  // ============================================================================

  class MiraAnimationController {
    constructor(initialState = "IDLE", eventBus = null) {
      this.currentState = (initialState || "IDLE").toUpperCase();
      this.previousState = this.currentState;
      this.isPaused = false;

      this.eventBus = eventBus || new MiraEventBus();
      this.eyeController = new MiraEyeController();
      this.attentionController = new MiraAttentionController();
      this.lipSyncController = new MiraLipSyncController();

      this._setupEventListeners();
      this._applyStateConfiguration(this.currentState);
    }

    _setupEventListeners() {
      this.eventBus.subscribe("USER_STARTED_SPEAKING", () => {
        if (this.currentState === "SPEAKING") {
          this.interrupt();
        } else {
          this.startListening();
        }
      });
      this.eventBus.subscribe("USER_INTERRUPTED", () => this.interrupt());
      this.eventBus.subscribe("AI_PROCESSING", () => this.startThinking());
      this.eventBus.subscribe("AI_STARTED_SPEAKING", () => this.startSpeaking());
      this.eventBus.subscribe("AI_STOPPED_SPEAKING", () => this.stopSpeaking());
      this.eventBus.subscribe("EMERGENCY_DETECTED", () => this.showEmergency());
      this.eventBus.subscribe("TRIAGE_ESCALATING", () => this.setState("ESCALATING"));
      this.eventBus.subscribe("CLINICAL_CONCERN_RAISED", () => this.showConcern());
      this.eventBus.subscribe("RESET_REQUESTED", () => this.reset());
    }

    get currentPriority() {
      return STATE_PRIORITIES[this.currentState] || 10;
    }

    setState(stateKey, force = false) {
      const upper = (stateKey || "IDLE").toUpperCase();
      if (!MIRA_STATES[upper]) return false;
      if (upper === this.currentState) return true;

      const targetPriority = STATE_PRIORITIES[upper] || 10;
      const currentPriority = this.currentPriority;

      // Enforce strict priority hierarchy unless explicitly forced
      if (!force && targetPriority < currentPriority) {
        return false;
      }

      this.previousState = this.currentState;
      this.currentState = upper;
      this._applyStateConfiguration(this.currentState);
      return true;
    }

    _applyStateConfiguration(stateKey) {
      const config = MIRA_STATES[stateKey] || MIRA_STATES.IDLE;

      // 1. Eye Subsystem
      this.eyeController.lookAt(config.gaze);
      this.eyeController.baseBlinkInterval = config.blinkInterval;
      this.eyeController.squintWeight = (stateKey === "THINKING" || stateKey === "CONCERNED") ? 0.2 : 0.0;

      // 2. Attention Subsystem
      this.attentionController.breathingRateCpm = config.breathingCpm;
      this.attentionController.targetPostureLean = config.lean;
      this.attentionController.targetRoll = config.tilt;
      this.attentionController.setTarget(config.gaze === "AWAY" ? "UP" : "USER");

      // 3. Lip Sync & Actions
      if (stateKey === "LISTENING") {
        this.attentionController.triggerListeningNod();
        this.lipSyncController.stop();
      } else if (stateKey === "SPEAKING") {
        this.lipSyncController.startSpeakingCadence();
      } else {
        this.lipSyncController.stop();
      }
    }

    // High-Level Public API
    playGreeting() { this.setState("GREETING", true); }
    startListening() { this.setState("LISTENING"); }
    startThinking() { this.setState("THINKING"); }
    startSpeaking() { this.setState("SPEAKING"); }
    stopSpeaking() {
      this.lipSyncController.stop();
      if (this.currentState === "SPEAKING") {
        this.setState("IDLE", true);
      }
    }
    showConcern() { this.setState("CONCERNED"); }
    showEmergency() { this.setState("EMERGENCY", true); }
    returnToIdle() { this.setState("IDLE", true); }
    lookAtUser() { this.eyeController.lookAtUser(); this.attentionController.orientToUser(); }
    lookAtScreen() { this.eyeController.lookAtScreen(); this.attentionController.orientToScreen(); }
    lookAway() { this.eyeController.lookAway(); }
    blink() { this.eyeController.blink(); }

    interrupt() {
      // Patient barge-in: instant stop speaking & snap to attentive listening
      this.lipSyncController.stop();
      this.setState("LISTENING", true);
      this.attentionController.triggerListeningNod();
    }

    reset() {
      this.currentState = "IDLE";
      this.previousState = "IDLE";
      this.isPaused = false;
      this.eyeController.reset();
      this.attentionController.reset();
      this.lipSyncController.stop();
      this._applyStateConfiguration("IDLE");
    }

    pause() { this.isPaused = true; }
    resume() { this.isPaused = false; }

    update(dt) {
      if (this.isPaused) {
        return {
          state: this.currentState,
          priority: this.currentPriority,
          isPaused: true,
          eye: this.eyeController.update(0.0),
          attention: this.attentionController.update(0.0),
          lipSync: this.lipSyncController.update(0.0),
        };
      }

      const eye = this.eyeController.update(dt);
      const attention = this.attentionController.update(dt);
      const lipSync = this.lipSyncController.update(dt);

      return {
        state: this.currentState,
        priority: this.currentPriority,
        isPaused: false,
        eye,
        attention,
        lipSync,
      };
    }
  }

  // ============================================================================
  // Custom Web Component: <mira-character>
  // ============================================================================

  class MiraCharacterComponent extends HTMLElement {
    static get observedAttributes() {
      return [
        "state",
        "size",
        "visibility",
        "interaction-enabled",
        "animation-enabled",
        "expression-state",
        "asset-src",
      ];
    }

    constructor() {
      super();
      this.controller = new MiraAnimationController("IDLE");
      this._size = "responsive";
      this._visibility = true;
      this._interactionEnabled = true;
      this._animationEnabled = true;
      this._expressionState = "calm";
      this._assetSrc = CANONICAL_ASSET_URL;
      this._isRendered = false;

      this._rafId = null;
      this._lastTimestamp = 0;
      this._observer = null;
    }

    connectedCallback() {
      if (!this._isRendered) {
        this._render();
        this._isRendered = true;
      }
      this._updateFromAttributes();
      this._setupLifecycleObserver();
      this._startAnimationLoop();
    }

    disconnectedCallback() {
      this._stopAnimationLoop();
      if (this._observer) {
        this._observer.disconnect();
        this._observer = null;
      }
    }

    attributeChangedCallback(name, oldValue, newValue) {
      if (oldValue === newValue) return;
      switch (name) {
        case "state":
          if (newValue) {
            this.controller.setState(newValue, true);
            this._updateStateUI();
          }
          break;
        case "size":
          this._size = newValue || "responsive";
          break;
        case "visibility":
          this._visibility = newValue !== "false";
          if (!this._visibility) this.controller.pause();
          else this.controller.resume();
          break;
        case "interaction-enabled":
          this._interactionEnabled = newValue !== "false";
          break;
        case "animation-enabled":
          this._animationEnabled = newValue !== "false";
          if (!this._animationEnabled) this.controller.pause();
          else this.controller.resume();
          break;
        case "expression-state":
          this._expressionState = newValue || "calm";
          break;
        case "asset-src":
          if (newValue && this._imgElement) {
            this._assetSrc = newValue;
            this._imgElement.src = this._assetSrc;
          }
          break;
      }
    }

    // Public Getters & Setters
    get state() { return this.controller.currentState; }
    set state(val) {
      this.controller.setState(val, true);
      this.setAttribute("state", this.controller.currentState);
      this._updateStateUI();
    }

    get size() { return this._size; }
    set size(val) { this.setAttribute("size", val); }

    get visibility() { return this._visibility; }
    set visibility(val) { this.setAttribute("visibility", String(val)); }

    get interactionEnabled() { return this._interactionEnabled; }
    set interactionEnabled(val) { this.setAttribute("interaction-enabled", String(val)); }

    get animationEnabled() { return this._animationEnabled; }
    set animationEnabled(val) { this.setAttribute("animation-enabled", String(val)); }

    _updateFromAttributes() {
      if (this.hasAttribute("state")) {
        this.controller.setState(this.getAttribute("state"), true);
      }
      if (this.hasAttribute("size")) {
        this._size = this.getAttribute("size");
      }
      if (this.hasAttribute("asset-src")) {
        this._assetSrc = this.getAttribute("asset-src");
      }
      this._updateStateUI();
    }

    _setupLifecycleObserver() {
      // Pause animation when character is offscreen (Lifecycle optimization)
      if (typeof window !== "undefined" && "IntersectionObserver" in window) {
        this._observer = new IntersectionObserver((entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              this.controller.resume();
            } else {
              this.controller.pause();
            }
          });
        }, { threshold: 0.1 });
        this._observer.observe(this);
      }

      // Pause when browser tab is inactive
      if (typeof document !== "undefined") {
        document.addEventListener("visibilitychange", () => {
          if (document.hidden) {
            this.controller.pause();
          } else {
            this.controller.resume();
          }
        });
      }
    }

    _render() {
      const container = document.createElement("div");
      container.className = "mira-character-container";

      container.innerHTML = `
        <div class="mira-portrait-canvas" id="portraitCanvas">
          <!-- Multi-Layer Visual Architecture Stack -->
          <div class="mira-layers-stack" id="layersStack">
            <div class="mira-layer mira-layer-background" data-layer="BACKGROUND"></div>
            <div class="mira-layer mira-layer-body" data-layer="BODY"></div>
            <div class="mira-layer mira-layer-uniform" data-layer="UNIFORM"></div>
            <div class="mira-layer mira-layer-head" data-layer="HEAD"></div>
            <div class="mira-layer mira-layer-hair" data-layer="HAIR"></div>
            
            <!-- Layer 50: Canonical Face & Visual Identity Anchor -->
            <div class="mira-layer mira-layer-face" data-layer="FACE">
              <img 
                class="mira-canonical-image" 
                src="${this._assetSrc}" 
                alt="MIRA — AI Nurse Assistant" 
                draggable="false"
              />
            </div>
            
            <!-- Layer 60: Dynamic Eyelid & Ocular Overlay (Anatomically Calibrated) -->
            <div class="mira-layer mira-layer-eyes" data-layer="EYES" id="layerEyes">
              <!-- Left Eye (Viewer's Left, anatomical right) -->
              <div class="mira-eye-aperture mira-eye-left">
                <div class="mira-eyelid-curtain" id="eyelidLeft"></div>
              </div>
              <!-- Right Eye (Viewer's Right, anatomical left) -->
              <div class="mira-eye-aperture mira-eye-right">
                <div class="mira-eyelid-curtain" id="eyelidRight"></div>
              </div>
            </div>

            <div class="mira-layer mira-layer-eyebrows" data-layer="EYEBROWS" id="layerEyebrows"></div>

            <!-- Layer 80: Dynamic Phonetic Viseme Mouth Overlay -->
            <div class="mira-layer mira-layer-mouth" data-layer="MOUTH" id="layerMouth">
              <div class="mira-mouth-aperture" id="mouthAperture"></div>
            </div>

            <div class="mira-layer mira-layer-accessories" data-layer="ACCESSORIES"></div>
          </div>

          <!-- Subtle Clinical Ambient Halo -->
          <div class="mira-state-halo" id="stateHalo"></div>

          <!-- Header Overlay: Branding & State Pill -->
          <div class="mira-badge-overlay">
            <div class="mira-identity-tag">
              <span class="mira-logo-dot"></span>
              <span class="mira-logo-text">MIRA</span>
              <span class="mira-credential-text">AI NURSE ASSISTANT</span>
            </div>
            <div class="mira-state-pill" id="miraStatePill">
              <span class="mira-state-indicator-dot" id="miraDot"></span>
              <span id="miraStateLabel">IDLE</span>
            </div>
          </div>

          <!-- Bedside Status Info -->
          <div class="mira-bottom-bar">
            <div class="mira-info-cluster">
              <div class="mira-name-label">
                MIRA
                <span class="mira-accent-badge">CLINICAL COMPANION</span>
              </div>
              <div class="mira-clinical-intent" id="miraIntentLabel">
                Observing bedside and ready to assist
              </div>
            </div>
            <div class="mira-version-label">
              MODEL: MIRA_FACE_MODEL_v1
            </div>
          </div>
        </div>
      `;

      this.appendChild(container);

      this._layersStack = this.querySelector("#layersStack");
      this._imgElement = this.querySelector(".mira-canonical-image");
      this._eyelidLeft = this.querySelector("#eyelidLeft");
      this._eyelidRight = this.querySelector("#eyelidRight");
      this._mouthAperture = this.querySelector("#mouthAperture");
      this._statePill = this.querySelector("#miraStatePill");
      this._stateLabel = this.querySelector("#miraStateLabel");
      this._intentLabel = this.querySelector("#miraIntentLabel");
      this._dot = this.querySelector("#miraDot");

      // Fallback asset loader if needed
      if (this._imgElement) {
        this._imgElement.onerror = () => {
          if (this._imgElement.src !== FALLBACK_ASSET_URL) {
            this._imgElement.src = FALLBACK_ASSET_URL;
          }
        };
      }
    }

    _updateStateUI() {
      const stateKey = this.controller.currentState;
      const meta = MIRA_STATES[stateKey] || MIRA_STATES.IDLE;

      if (this._stateLabel) this._stateLabel.textContent = meta.name.toUpperCase();
      if (this._intentLabel) this._intentLabel.textContent = meta.intent;
      if (this._dot) this._dot.style.backgroundColor = meta.accent;

      this.style.setProperty("--state-accent", meta.accent);

      this.dispatchEvent(
        new CustomEvent("mira-state-change", {
          bubbles: true,
          composed: true,
          detail: {
            state: stateKey,
            priority: this.controller.currentPriority,
            meta,
            timestamp: Date.now(),
          },
        })
      );
    }

    _startAnimationLoop() {
      const loop = (timestamp) => {
        if (!this._lastTimestamp) this._lastTimestamp = timestamp;
        const dt = Math.min(0.1, (timestamp - this._lastTimestamp) / 1000.0);
        this._lastTimestamp = timestamp;

        if (this._animationEnabled && !this.controller.isPaused) {
          const frame = this.controller.update(dt);
          this._applyFrame(frame);
        }

        this._rafId = requestAnimationFrame(loop);
      };
      this._rafId = requestAnimationFrame(loop);
    }

    _stopAnimationLoop() {
      if (this._rafId) {
        cancelAnimationFrame(this._rafId);
        this._rafId = null;
      }
    }

    _applyFrame(frame) {
      // 1. Apply Natural Respiratory Rhythm & Subtle Head Orientation
      // Strictly NO whole-character bouncing or zooming; uses micro-perspective transform
      if (this._layersStack) {
        const att = frame.attention;
        const pitch = att.pitch.toFixed(2);
        const yaw = att.yaw.toFixed(2);
        const roll = att.roll.toFixed(2);
        const by = att.breathingOffsetY.toFixed(2);
        const bs = att.breathingScale.toFixed(4);

        this._layersStack.style.transform = `
          perspective(1000px)
          rotateX(${pitch}deg)
          rotateY(${yaw}deg)
          rotateZ(${roll}deg)
          translateY(${by}px)
          scale(${bs})
        `;
      }

      // 2. Apply Biological Eyelid Occlusion on Blinks
      const blink = frame.eye.blinkWeight;
      if (this._eyelidLeft && this._eyelidRight) {
        if (blink > 0.01) {
          const lidPercent = (blink * 100).toFixed(1);
          this._eyelidLeft.style.height = `${lidPercent}%`;
          this._eyelidRight.style.height = `${lidPercent}%`;
          this._eyelidLeft.style.opacity = "1";
          this._eyelidRight.style.opacity = "1";
        } else {
          this._eyelidLeft.style.height = "0%";
          this._eyelidRight.style.height = "0%";
          this._eyelidLeft.style.opacity = "0";
          this._eyelidRight.style.opacity = "0";
        }
      }

      // 3. Apply Phonetic Viseme Mouth Articulation
      if (this._mouthAperture) {
        const lip = frame.lipSync;
        if (lip.isActive && lip.jawOpen > 0.02) {
          const h = (lip.jawOpen * 12).toFixed(1); // Subtle natural opening (0-12px)
          const w = (28 + lip.lipWide * 6).toFixed(1);
          this._mouthAperture.style.height = `${h}px`;
          this._mouthAperture.style.width = `${w}px`;
          this._mouthAperture.style.opacity = "0.75";
        } else {
          this._mouthAperture.style.height = "0px";
          this._mouthAperture.style.opacity = "0";
        }
      }
    }
  }

  // Register Web Component if customElements is supported
  if (typeof window !== "undefined" && window.customElements) {
    if (!customElements.get("mira-character")) {
      customElements.define("mira-character", MiraCharacterComponent);
    }
  }

  // Standalone Global API
  window.MiraCharacter = {
    Component: MiraCharacterComponent,
    STATES: MIRA_STATES,
    STATE_PRIORITIES,
    CANONICAL_MODEL: "MIRA_FACE_MODEL_v1",
    EventBus: MiraEventBus,
    AnimationController: MiraAnimationController,
    EyeController: MiraEyeController,
    AttentionController: MiraAttentionController,
    LipSyncController: MiraLipSyncController,
    create: function (options = {}) {
      const el = document.createElement("mira-character");
      if (options.state) el.setAttribute("state", options.state);
      if (options.size) el.setAttribute("size", options.size);
      if (options.visibility !== undefined) el.setAttribute("visibility", String(options.visibility));
      if (options.interactionEnabled !== undefined) el.setAttribute("interaction-enabled", String(options.interactionEnabled));
      if (options.animationEnabled !== undefined) el.setAttribute("animation-enabled", String(options.animationEnabled));
      if (options.expressionState) el.setAttribute("expression-state", options.expressionState);
      return el;
    },
  };
})();
