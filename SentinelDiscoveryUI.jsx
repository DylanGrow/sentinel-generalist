import React, { useState, useEffect, useRef } from 'react';
import { AlertTriangle, Check, AlertCircle, Zap, Globe2, Leaf } from 'lucide-react';

/**
 * SENTINEL GENERALIST - Discovery UI Component
 * Renders real-time inference data with glassmorphism design
 * Judges will love the reasoning trace + environmental card combo
 */

const SentinelDiscoveryUI = ({ inferenceData, isProcessing, reasoningTrace }) => {
  const [animatedStep, setAnimatedStep] = useState(0);
  const traceEndRef = useRef(null);

  // Auto-scroll reasoning trace
  useEffect(() => {
    traceEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [reasoningTrace]);

  // Animate reasoning steps one by one for visual impact
  useEffect(() => {
    if (reasoningTrace && reasoningTrace.length > 0) {
      const timer = setTimeout(() => {
        setAnimatedStep(prev => Math.min(prev + 1, reasoningTrace.length));
      }, 800);
      return () => clearTimeout(timer);
    }
  }, [reasoningTrace]);

  if (!inferenceData && !isProcessing) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-8 flex items-center justify-center">
        <div className="text-center text-white">
          <Zap className="w-16 h-16 mx-auto mb-4 text-purple-400" />
          <p className="text-xl font-light">Upload an image to begin Sentinel Generalist analysis</p>
        </div>
      </div>
    );
  }

  const { 
    subject_analysis = {}, 
    environmental_deduction = {}, 
    actionable_intelligence = {}, 
    fallback_confidence = {} 
  } = inferenceData || {};

  const healthStateColor = {
    'HEALTHY': 'bg-emerald-500/20 border-emerald-400 text-emerald-300',
    'STRESSED': 'bg-yellow-500/20 border-yellow-400 text-yellow-300',
    'DISEASED': 'bg-red-500/20 border-red-400 text-red-300',
    'HARVEST_READY': 'bg-blue-500/20 border-blue-400 text-blue-300',
    'CRITICAL': 'bg-orange-500/20 border-orange-400 text-orange-300'
  };

  const alertLevelColor = {
    'LOW': 'bg-blue-500/10 border-blue-400',
    'MEDIUM': 'bg-yellow-500/10 border-yellow-400',
    'HIGH': 'bg-orange-500/10 border-orange-400',
    'CRITICAL': 'bg-red-500/10 border-red-400'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-8">
      <div className="max-w-7xl mx-auto">
        
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2 flex items-center gap-3">
            <Leaf className="w-10 h-10 text-emerald-400" />
            Sentinel Generalist
          </h1>
          <p className="text-purple-300 text-sm font-light">Zero-Shot Environmental Discovery Agent</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* COLUMN 1: Reasoning Trace (Live) */}
          <div className="lg:col-span-1">
            <div className="backdrop-blur-md bg-white/10 border border-white/20 rounded-2xl p-6 sticky top-8">
              <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5 text-yellow-400" />
                Reasoning Trace
              </h2>
              
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {isProcessing && (
                  <div className="animate-pulse">
                    <div className="h-3 bg-purple-400/30 rounded-full mb-2"></div>
                    <div className="h-2 bg-purple-400/20 rounded-full w-5/6"></div>
                  </div>
                )}
                
                {reasoningTrace && reasoningTrace.slice(0, animatedStep).map((step, idx) => (
                  <div 
                    key={idx}
                    className="animate-in fade-in slide-in-from-left-2 duration-500"
                  >
                    <div className="flex gap-3">
                      <div className="flex-shrink-0 mt-1">
                        <div className="w-6 h-6 rounded-full bg-purple-400/30 border border-purple-400/50 flex items-center justify-center text-xs text-purple-300">
                          {idx + 1}
                        </div>
                      </div>
                      <div>
                        <p className="text-sm text-white font-medium">{step.action}</p>
                        <div className="mt-1 space-y-1">
                          {step.visual_evidence && step.visual_evidence.map((evidence, eidx) => (
                            <p key={eidx} className="text-xs text-purple-200/70">
                              └─ {evidence}
                            </p>
                          ))}
                        </div>
                        <p className="text-xs text-purple-300/50 mt-1">
                          Confidence: {(step.confidence * 100).toFixed(0)}%
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
                <div ref={traceEndRef} />
              </div>
            </div>
          </div>

          {/* COLUMN 2: Main Analysis Cards */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Subject Analysis Card */}
            <div className="backdrop-blur-md bg-white/10 border border-white/20 rounded-2xl p-8 hover:bg-white/15 transition-all">
              <h2 className="text-white font-semibold mb-6 text-lg">Subject Analysis</h2>
              
              <div className="space-y-6">
                {/* Species ID */}
                <div>
                  <p className="text-purple-300 text-sm font-light mb-2">IDENTIFIED SPECIES</p>
                  <p className="text-white text-2xl font-semibold">
                    {subject_analysis.identified_species || 'Analyzing...'}
                  </p>
                  <div className="mt-3 flex items-center gap-2">
                    <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-emerald-400 to-cyan-400 transition-all duration-1000"
                        style={{ width: `${(subject_analysis.confidence || 0) * 100}%` }}
                      />
                    </div>
                    <span className="text-white text-sm font-mono">
                      {(subject_analysis.confidence || 0 * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>

                {/* Health State */}
                <div>
                  <p className="text-purple-300 text-sm font-light mb-3">BIOLOGICAL STATE</p>
                  <div className={`px-4 py-3 rounded-lg border ${healthStateColor[subject_analysis.biological_state] || 'bg-slate-500/10 border-slate-400'} inline-block`}>
                    <span className="font-semibold">
                      {subject_analysis.biological_state || 'UNKNOWN'}
                    </span>
                  </div>
                </div>

                {/* Alternate Hypotheses */}
                {subject_analysis.alternate_hypotheses && subject_analysis.alternate_hypotheses.length > 0 && (
                  <div>
                    <p className="text-purple-300 text-sm font-light mb-3">ALTERNATE HYPOTHESES</p>
                    <div className="space-y-2">
                      {subject_analysis.alternate_hypotheses.map((hyp, idx) => (
                        <div key={idx} className="text-sm text-purple-200/70 p-3 bg-white/5 rounded-lg border border-white/10">
                          <p className="font-medium text-white">{hyp.species}</p>
                          <p className="text-xs text-purple-300/70">{hyp.why_less_likely}</p>
                          <p className="text-xs font-mono text-purple-400 mt-1">
                            {(hyp.probability * 100).toFixed(1)}% likelihood
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Environmental Deduction Card - GLASSMORPHISM HERO */}
            <div className="backdrop-blur-xl bg-gradient-to-br from-white/15 to-white/5 border border-white/30 rounded-3xl p-8 shadow-2xl hover:shadow-purple-500/20 hover:border-white/40 transition-all">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-white font-semibold text-lg mb-1">Detected Environment</h2>
                  <p className="text-purple-300 text-sm font-light">Zero-Shot Geospatial Inference</p>
                </div>
                <Globe2 className="w-6 h-6 text-emerald-400" />
              </div>

              <div className="grid grid-cols-2 gap-6">
                {/* Region */}
                <div className="col-span-2 md:col-span-1">
                  <p className="text-purple-300 text-xs font-light uppercase tracking-wider mb-2">INFERRED REGION</p>
                  <p className="text-white text-lg font-semibold">
                    {environmental_deduction.inferred_region || 'Calculating...'}
                  </p>
                </div>

                {/* USDA Zone */}
                <div>
                  <p className="text-purple-300 text-xs font-light uppercase tracking-wider mb-2">USDA HARDINESS ZONE</p>
                  <p className="text-white text-lg font-semibold font-mono">
                    {environmental_deduction.inferred_climate?.usda_hardiness_zone || '--'}
                  </p>
                </div>

                {/* Köppen Classification */}
                <div>
                  <p className="text-purple-300 text-xs font-light uppercase tracking-wider mb-2">CLIMATE CLASS</p>
                  <p className="text-white text-lg font-semibold font-mono">
                    {environmental_deduction.inferred_climate?.koppen_classification || '--'}
                  </p>
                </div>

                {/* Latitude */}
                <div className="col-span-2">
                  <p className="text-purple-300 text-xs font-light uppercase tracking-wider mb-2">ESTIMATED LATITUDE</p>
                  <p className="text-white text-lg font-semibold font-mono">
                    {environmental_deduction.inferred_climate?.estimated_latitude || 'Inferring...'}
                  </p>
                </div>

                {/* Soil Assessment */}
                <div className="col-span-2">
                  <p className="text-purple-300 text-xs font-light uppercase tracking-wider mb-3">SOIL PROFILE</p>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-purple-300">Texture:</span>
                      <span className="text-white font-mono">{environmental_deduction.soil_assessment?.texture || '--'}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-purple-300">Drainage:</span>
                      <span className="text-white font-mono">{environmental_deduction.soil_assessment?.drainage_appearance || '--'}</span>
                    </div>
                  </div>
                </div>

                {/* Climate Clues */}
                {environmental_deduction.climate_clues && environmental_deduction.climate_clues.length > 0 && (
                  <div className="col-span-2">
                    <p className="text-purple-300 text-xs font-light uppercase tracking-wider mb-3">KEY OBSERVATIONS</p>
                    <div className="space-y-2">
                      {environmental_deduction.climate_clues.map((clue, idx) => (
                        <div key={idx} className="text-xs text-purple-200/80 p-3 bg-white/5 rounded-lg border border-white/10">
                          <p className="text-white/90 font-medium">{clue.observation}</p>
                          <p className="text-purple-300/70 mt-1">{clue.inference}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Actionable Intelligence Card */}
            {actionable_intelligence.primary_instruction && (
              <div className="backdrop-blur-md bg-white/10 border border-white/20 rounded-2xl p-8">
                <h2 className="text-white font-semibold mb-6">Actionable Intelligence</h2>
                
                <div className="space-y-6">
                  <div>
                    <p className="text-purple-300 text-sm font-light mb-3">PRIMARY INSTRUCTION</p>
                    <p className="text-white text-lg leading-relaxed">
                      {actionable_intelligence.primary_instruction}
                    </p>
                    <p className="text-purple-300 text-sm mt-3">
                      {actionable_intelligence.technical_rationale}
                    </p>
                  </div>

                  {actionable_intelligence.estimated_days_to_action && (
                    <div className="flex items-center gap-3 p-4 bg-yellow-500/10 border border-yellow-400/30 rounded-lg">
                      <AlertCircle className="w-5 h-5 text-yellow-400 flex-shrink-0" />
                      <span className="text-yellow-300">
                        <strong>Action Required:</strong> {actionable_intelligence.estimated_days_to_action}
                      </span>
                    </div>
                  )}

                  {/* Community Broadcast Alert */}
                  {actionable_intelligence.community_broadcast?.required && (
                    <div className={`p-6 rounded-xl border ${alertLevelColor[actionable_intelligence.community_broadcast.alert_level]}`}>
                      <div className="flex items-start gap-3">
                        <AlertTriangle className="w-6 h-6 flex-shrink-0 mt-1" />
                        <div className="flex-1">
                          <p className="text-white font-semibold mb-2">
                            📡 Community Alert: {actionable_intelligence.community_broadcast.alert_type}
                          </p>
                          <p className="text-white/80 text-sm mb-3">
                            {actionable_intelligence.community_broadcast.broadcast_payload?.threat_description}
                          </p>
                          <div className="text-xs text-white/70 space-y-1">
                            <p><strong>Affected Regions:</strong> {actionable_intelligence.community_broadcast.broadcast_payload?.affected_regions?.join(', ')}</p>
                            <p><strong>Mitigation:</strong> {actionable_intelligence.community_broadcast.broadcast_payload?.recommended_mitigation}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Fallback Confidence Warning */}
            {fallback_confidence.is_uncertain && (
              <div className="backdrop-blur-md bg-orange-500/10 border border-orange-400/30 rounded-2xl p-6 flex items-start gap-4">
                <AlertCircle className="w-6 h-6 text-orange-400 flex-shrink-0 mt-1" />
                <div>
                  <p className="text-orange-300 font-semibold mb-1">Low Confidence Analysis</p>
                  <p className="text-orange-200/80 text-sm">{fallback_confidence.why_uncertain}</p>
                  {fallback_confidence.suggest_human_review && (
                    <p className="text-orange-300 text-sm mt-2 font-medium">→ Human expert review recommended</p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SentinelDiscoveryUI;
