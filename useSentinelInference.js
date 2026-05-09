/**
 * useSentinelInference - React Hook for Streaming Sentinel Analysis
 * 
 * Handles:
 * - File upload to DigitalOcean MI300X backend
 * - Real-time streaming of reasoning trace
 * - Progressive UI updates
 * - Error handling
 */

import { useState, useCallback, useRef } from 'react';

export const useSentinelInference = (onUpdate) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [inferenceData, setInferenceData] = useState(null);
  const [reasoningTrace, setReasoningTrace] = useState([]);
  const [error, setError] = useState(null);
  const abortControllerRef = useRef(null);

  const analyzeImage = useCallback(async (file) => {
    // Reset state
    setIsProcessing(true);
    setError(null);
    setReasoningTrace([]);
    setInferenceData(null);
    abortControllerRef.current = new AbortController();

    try {
      // 1. Prepare form data
      const formData = new FormData();
      formData.append('file', file);

      // 2. Stream from backend
      const response = await fetch('/api/sentinel/analyze', {
        method: 'POST',
        body: formData,
        signal: abortControllerRef.current.signal,
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.statusText}`);
      }

      // 3. Consume streaming response (NDJSON format)
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        // Append chunk to buffer
        buffer += decoder.decode(value, { stream: true });

        // Process complete lines
        const lines = buffer.split('\n');
        buffer = lines[lines.length - 1]; // Keep incomplete line in buffer

        for (const line of lines.slice(0, -1)) {
          if (!line.trim()) continue;

          try {
            const update = JSON.parse(line);

            if (update.type === 'reasoning_step') {
              // Add step to trace with animation
              setReasoningTrace((prev) => [...prev, update.step]);
              
              // Callback for custom handling
              if (onUpdate) {
                onUpdate({
                  type: 'step',
                  step: update.step,
                  stepNumber: update.step_number,
                  totalSteps: update.total_steps,
                });
              }
            } else if (update.type === 'complete') {
              // Full inference data received
              setInferenceData(update.data);
              
              if (onUpdate) {
                onUpdate({
                  type: 'complete',
                  data: update.data,
                });
              }
            } else if (update.type === 'error') {
              throw new Error(update.message);
            }
          } catch (e) {
            console.error('Failed to parse streaming update:', e);
          }
        }
      }

      // Process final buffer
      if (buffer.trim()) {
        try {
          const update = JSON.parse(buffer);
          if (update.type === 'complete') {
            setInferenceData(update.data);
          }
        } catch (e) {
          console.error('Failed to parse final buffer:', e);
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError(err.message);
        if (onUpdate) {
          onUpdate({ type: 'error', message: err.message });
        }
      }
    } finally {
      setIsProcessing(false);
    }
  }, [onUpdate]);

  const cancel = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsProcessing(false);
    }
  }, []);

  const reset = useCallback(() => {
    setInferenceData(null);
    setReasoningTrace([]);
    setError(null);
    setIsProcessing(false);
  }, []);

  return {
    analyzeImage,
    isProcessing,
    inferenceData,
    reasoningTrace,
    error,
    cancel,
    reset,
  };
};

/**
 * Example Usage in a React Component:
 * 
 * function MyDemoComponent() {
 *   const { analyzeImage, isProcessing, inferenceData, reasoningTrace } = 
 *     useSentinelInference((update) => {
 *       if (update.type === 'step') {
 *         console.log(`Step ${update.stepNumber}: ${update.step.action}`);
 *       }
 *     });
 *
 *   const handleFileUpload = async (e) => {
 *     const file = e.target.files[0];
 *     if (file) {
 *       await analyzeImage(file);
 *     }
 *   };
 *
 *   return (
 *     <div>
 *       <input 
 *         type="file" 
 *         onChange={handleFileUpload}
 *         disabled={isProcessing}
 *       />
 *       {isProcessing && <p>Analyzing...</p>}
 *       {inferenceData && <SentinelDiscoveryUI inferenceData={inferenceData} reasoningTrace={reasoningTrace} />}
 *     </div>
 *   );
 * }
 */
