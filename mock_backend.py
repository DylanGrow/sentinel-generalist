"""
SENTINEL GENERALIST v3.0 - Mock Backend
Simulates the full AI response for local development & demo fallback.
When deployed on MI300X, replace this with sentinel_backend.py
"""

import json
import asyncio
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# MOCK DATA — Matches the v3.0 system prompt output schema exactly
# =============================================================================

MOCK_REASONING_TRACE = [
    {
        "step": 1,
        "action": "Initial scan — Identifying primary subject in frame",
        "visual_evidence": [
            "Single plant centered in raised bed",
            "Wooden garden border visible",
            "Residential backyard setting"
        ],
        "confidence": 0.96
    },
    {
        "step": 2,
        "action": "Species identification — Analyzing leaf morphology and fruit",
        "visual_evidence": [
            "Compound pinnate leaves with serrated leaflets",
            "Green immature fruit clusters, round shape ~3cm diameter",
            "Indeterminate growth habit with visible suckers"
        ],
        "confidence": 0.94
    },
    {
        "step": 3,
        "action": "Growth stage assessment — Evaluating maturity indicators",
        "visual_evidence": [
            "Yellow flowers still present on upper trusses",
            "First fruit set on lower trusses, green and firm",
            "Plant height ~90cm, staked with twine"
        ],
        "confidence": 0.91
    },
    {
        "step": 4,
        "action": "Soil and environment scan — Analyzing growing medium",
        "visual_evidence": [
            "Dark brown soil with visible compost fragments",
            "Reddish-brown undertone (Munsell 7.5YR 3/4)",
            "Straw mulch partially covering surface",
            "No visible standing water"
        ],
        "confidence": 0.87
    },
    {
        "step": 5,
        "action": "Light assessment — Analyzing shadows and leaf orientation",
        "visual_evidence": [
            "Sharp shadow cast at ~35° angle, indicating midday summer sun",
            "No leaf scorching or bleaching observed",
            "Leaves oriented upward, not reaching/stretching",
            "Fence shadow visible on east side of bed"
        ],
        "confidence": 0.84
    },
    {
        "step": 6,
        "action": "Nutrient status check — Examining leaf coloration patterns",
        "visual_evidence": [
            "Lower leaves showing uniform yellowing (oldest leaves first)",
            "Upper canopy dark green and vigorous",
            "No purple tinting on stems or undersides",
            "Slight interveinal chlorosis on mid-canopy leaves"
        ],
        "confidence": 0.88
    },
    {
        "step": 7,
        "action": "Water status evaluation — Checking turgor and soil moisture",
        "visual_evidence": [
            "Leaves fully turgid, no wilting",
            "Soil surface slightly crusted between mulch gaps",
            "No edema or waterlogging signs"
        ],
        "confidence": 0.90
    },
    {
        "step": 8,
        "action": "Pest and disease scan — Checking for pathology indicators",
        "visual_evidence": [
            "Concentric ring lesions on 2 lower leaves (target spot pattern)",
            "No visible insects or webbing",
            "Lesions confined to lower canopy, not systemic",
            "Brown necrotic tissue with yellow halo"
        ],
        "confidence": 0.91
    },
    {
        "step": 9,
        "action": "Companion plant assessment — Scanning nearby plantings",
        "visual_evidence": [
            "Basil plant visible 30cm to the right (beneficial companion)",
            "No marigolds or other pest-repellent companions detected",
            "Grass weeds emerging at bed edge"
        ],
        "confidence": 0.82
    },
    {
        "step": 10,
        "action": "Geospatial inference — Determining location from all clues",
        "visual_evidence": [
            "Wooden fence style: North American suburban",
            "Grass type: Cool-season fescue blend",
            "Sun angle + shadow length = ~42-48°N latitude",
            "Plant maturity for calendar date = Zone 6b-7a growing season"
        ],
        "confidence": 0.83
    }
]

MOCK_FULL_RESPONSE = {
    "inference_metadata": {
        "engine": "AMD_ROCM_7.0_HuggingFace_Optimum",
        "model_id": "Qwen2.5-VL-7B-Instruct-AMD-Optimized",
        "processing_timestamp": "2026-05-08T21:30:00Z",
        "zero_shot_confidence_threshold": 0.72
    },
    "reasoning_trace": MOCK_REASONING_TRACE,
    "subject_analysis": {
        "identified_species": "Solanum lycopersicum (Heirloom Tomato — likely 'Brandywine')",
        "confidence": 0.94,
        "growth_stage": "FRUITING",
        "estimated_age": "8-10 weeks from transplant",
        "alternate_hypotheses": [
            {
                "species": "Solanum lycopersicum 'Cherokee Purple'",
                "probability": 0.12,
                "why_less_likely": "Leaf shape slightly broader than Cherokee Purple typical"
            }
        ],
        "biological_state": "STRESSED",
        "state_confidence": 0.88
    },
    "environmental_deduction": {
        "inferred_region": "Mid-Atlantic USA (likely Pennsylvania / New Jersey corridor)",
        "inferred_season": "SUMMER",
        "inferred_climate": {
            "koppen_classification": "Cfa (Humid Subtropical)",
            "usda_hardiness_zone": "7a",
            "estimated_latitude": "40.2°N ± 1.5°"
        },
        "climate_clues": [
            {
                "observation": "Cool-season grass in lawn, still green",
                "inference": "Temperate region, adequate summer rainfall",
                "confidence": 0.85
            },
            {
                "observation": "Shadow angle suggests high summer sun position",
                "inference": "Late June to mid-July timeframe at ~40°N",
                "confidence": 0.82
            }
        ],
        "soil_assessment": {
            "texture": "loam",
            "estimated_ph": "6.2-6.8 (slightly acidic to neutral)",
            "drainage_appearance": "well-drained",
            "organic_matter": "HIGH",
            "moisture_level": "SLIGHTLY_MOIST",
            "nutrient_visual_cues": "Dark color suggests good organic content, but yellowing lower leaves indicate mobile nutrient depletion",
            "recommended_amendments": [
                "Side-dress with balanced 10-10-10 fertilizer",
                "Add 1 inch of compost mulch around base",
                "Consider calcium supplement (crusite/gypsum) to prevent blossom end rot"
            ]
        }
    },
    "light_assessment": {
        "current_exposure": "FULL_SUN",
        "estimated_daily_sun_hours": 7.5,
        "ideal_for_species": "FULL_SUN",
        "is_adequate": True,
        "light_stress_signs": [],
        "recommendation": "Light exposure is excellent for tomatoes. The east-side fence shadow provides beneficial afternoon relief during heat waves."
    },
    "nutrient_analysis": {
        "overall_status": "DEFICIENT",
        "deficiencies_detected": [
            {
                "nutrient": "Nitrogen",
                "severity": "MODERATE",
                "visual_evidence": "Uniform yellowing of oldest leaves progressing upward — classic mobile nutrient deficiency",
                "remedy": "Side-dress with 2 tablespoons blood meal per plant, or water with fish emulsion (2 tbsp per gallon) weekly for 3 weeks"
            },
            {
                "nutrient": "Magnesium",
                "severity": "MILD",
                "visual_evidence": "Faint interveinal chlorosis on mid-canopy leaves — green veins with slight yellowing between",
                "remedy": "Foliar spray with 1 tablespoon Epsom salt per gallon of water, apply every 2 weeks"
            }
        ],
        "toxicity_signs": []
    },
    "watering_assessment": {
        "current_status": "OPTIMAL",
        "visual_evidence": [
            "Good leaf turgor, no wilting",
            "Soil surface slightly dry between mulch (normal)",
            "No signs of edema or overwatering"
        ],
        "recommendation": "Current watering appears adequate. Water deeply (1-1.5 inches) every 3-4 days at the base, avoiding foliage. Early morning is ideal.",
        "mulch_recommendation": "Increase straw mulch to 3-4 inches to retain moisture and suppress the weeds emerging at the bed edge."
    },
    "pest_disease_analysis": {
        "severity": "MODERATE",
        "identified_issues": [
            {
                "type": "FUNGAL",
                "name": "Alternaria solani — Early Blight",
                "confidence": 0.91,
                "visual_evidence": "Concentric ring (target-spot) lesions on lower leaves with yellow halo. Classic Early Blight presentation.",
                "organic_remedy": "Remove all affected lower leaves immediately. Apply copper fungicide (Bonide Copper Fungicide) every 7-10 days. Ensure good airflow by pruning lower suckers.",
                "chemical_remedy": "Chlorothalonil-based fungicide (Daconil) every 7 days during wet periods.",
                "prevention": "Mulch to prevent soil splash. Avoid overhead watering. Practice 3-year rotation away from Solanaceae."
            }
        ]
    },
    "companion_planting": {
        "recommended_companions": [
            {
                "plant": "Marigold (Tagetes)",
                "benefit": "Repels nematodes, whiteflies, and tomato hornworms. Releases thiopene into soil.",
                "placement": "Ring around base of tomato bed, 1 plant every 18 inches"
            },
            {
                "plant": "Nasturtium",
                "benefit": "Trap crop for aphids — they attack nasturtium first, leaving tomatoes alone",
                "placement": "Plant at ends of each row as sacrificial border"
            },
            {
                "plant": "Carrots",
                "benefit": "Loosen soil around tomato roots, attract parasitic wasps that kill hornworms",
                "placement": "Interplant between tomato stakes"
            },
            {
                "plant": "Borage",
                "benefit": "Attracts pollinators, repels tomato hornworm, improves flavor (folk claim, but pollinators are proven)",
                "placement": "One plant per 4-foot section of bed"
            }
        ],
        "antagonist_plants": [
            {
                "plant": "Fennel",
                "reason": "Releases allelopathic compounds that inhibit tomato growth. Keep at least 20 feet away."
            },
            {
                "plant": "Brassicas (Cabbage, Broccoli, Kale)",
                "reason": "Heavy feeders that compete for the same nutrients. Both are susceptible to similar soil pathogens."
            },
            {
                "plant": "Black Walnut (nearby trees)",
                "reason": "Juglone toxicity — tomatoes are extremely sensitive. Fatal within days if roots reach juglone zone."
            },
            {
                "plant": "Corn",
                "reason": "Both are heavy nitrogen feeders and attract the same pest (Helicoverpa zea — corn earworm/tomato fruitworm)."
            }
        ],
        "current_companions_in_image": "Basil detected ~30cm to the right — EXCELLENT companion. Basil repels aphids, thrips, and mosquitoes, and some growers report it improves tomato flavor. Spacing looks good."
    },
    "harvest_intelligence": {
        "estimated_days_to_harvest": 28,
        "harvest_readiness": "NOT_YET",
        "visual_harvest_cues": "Brandywine tomatoes are ready when they turn deep pink-red and yield slightly to thumb pressure. They will crack if left too long — harvest at first full color change.",
        "succession_planting": "After tomato harvest (late August), plant fall crop of lettuce, spinach, or radishes. Or sow a cover crop of crimson clover to fix nitrogen for next year."
    },
    "seasonal_planning": {
        "current_season_tasks": [
            "Prune suckers below first fruit truss for better airflow",
            "Apply nitrogen boost (fish emulsion or blood meal) this week",
            "Install drip irrigation if not already present to avoid wet foliage",
            "Scout for hornworms weekly — they appear mid-summer"
        ],
        "next_season_prep": "Plan fall garlic planting (October) in a different bed. Order cover crop seed (crimson clover or winter rye) for post-harvest.",
        "crop_rotation_note": "Solanaceae family (tomatoes, peppers, eggplant, potatoes). Do NOT plant any Solanaceae in this bed for 3 years. Follow with legumes (beans/peas) to restore nitrogen.",
        "frost_risk": "First frost estimated mid-October for Zone 7a. Plan to harvest all remaining fruit by early October or have row cover ready."
    },
    "actionable_intelligence": {
        "priority_actions": [
            {
                "urgency": "IMMEDIATE",
                "instruction": "Remove all lower leaves showing Early Blight lesions. Bag and dispose — do NOT compost.",
                "rationale": "Fungal spores spread via rain splash from infected foliage. Removing source material slows progression by 60-70%."
            },
            {
                "urgency": "THIS_WEEK",
                "instruction": "Apply fish emulsion (2 tbsp/gallon) to address nitrogen deficiency. Water at base of plant.",
                "rationale": "Lower leaf yellowing indicates the heavy fruit load is depleting nitrogen faster than soil can supply. Fruiting tomatoes need 2x the nitrogen of vegetative plants."
            },
            {
                "urgency": "THIS_WEEK",
                "instruction": "Add marigolds around the tomato bed perimeter.",
                "rationale": "No pest-repellent companions detected. Marigolds provide proven nematode suppression and whitefly deterrence."
            },
            {
                "urgency": "THIS_MONTH",
                "instruction": "Apply Epsom salt foliar spray for magnesium. Increase mulch depth to 3-4 inches.",
                "rationale": "Mild magnesium deficiency detected. Straw mulch will retain moisture, suppress weeds, and prevent soil splash that spreads blight spores."
            }
        ],
        "community_broadcast": {
            "required": True,
            "alert_level": "MEDIUM",
            "alert_type": "DISEASE",
            "broadcast_payload": {
                "threat_description": "Early Blight (Alternaria solani) confirmed in Zone 7a residential garden. Humid conditions likely accelerating spore dispersal.",
                "affected_regions": ["Mid-Atlantic USA", "Zone 7a gardens", "Delaware Valley"],
                "recommended_mitigation": "Preventative copper fungicide application. Increase plant spacing and avoid overhead irrigation.",
                "peer_network_action": "Monitor tomato plantings for concentric ring lesions on lower foliage. Report confirmed cases to strengthen regional tracking."
            }
        }
    },
    "beginner_planner": {
        "harvest_image_url": "/harvest_preview.png",
        "zone_summary": "You're in Zone 7a — warm summers, mild winters. One of the best zones for growing a huge variety of food! 🌞",
        "current_planting_window": "Early May is prime planting time! The last frost is behind you. Get warm-season crops in the ground now and you'll be harvesting by midsummer.",
        "plant_now": [
            {
                "name": "Cherry Tomatoes",
                "emoji": "🍅",
                "category": "VEGETABLE",
                "difficulty": "EASY",
                "days_to_harvest": 65,
                "why_now": "Perfect time to transplant — soil is warm enough and you'll get fruit by mid-July.",
                "beginner_tip": "Start with 'Sweet 100' or 'Sun Gold' varieties. They're incredibly forgiving and produce hundreds of tomatoes per plant."
            },
            {
                "name": "Zucchini",
                "emoji": "🥒",
                "category": "VEGETABLE",
                "difficulty": "EASY",
                "days_to_harvest": 50,
                "why_now": "Zucchini loves warm soil. Plant now and you'll have more than you know what to do with by late June.",
                "beginner_tip": "One plant is enough for a family of four. Seriously. Don't plant six unless you want to become the neighborhood zucchini dealer."
            },
            {
                "name": "Basil",
                "emoji": "🌿",
                "category": "HERB",
                "difficulty": "EASY",
                "days_to_harvest": 30,
                "why_now": "Basil thrives in summer heat. It also repels mosquitoes and pairs perfectly with your tomatoes.",
                "beginner_tip": "Pinch off flower buds as they appear — this keeps the plant bushy and producing leaves all summer long."
            },
            {
                "name": "Sunflowers",
                "emoji": "🌻",
                "category": "FLOWER",
                "difficulty": "EASY",
                "days_to_harvest": "70-80 days to bloom",
                "why_now": "Direct sow seeds now — they love the warming soil. Kids love watching these grow because they're so fast and dramatic.",
                "beginner_tip": "Plant along a north-facing fence so they don't shade your other plants. They can reach 8+ feet tall!"
            },
            {
                "name": "Marigolds",
                "emoji": "🏵️",
                "category": "FLOWER",
                "difficulty": "EASY",
                "days_to_harvest": "45-50 days to bloom",
                "why_now": "Your tomato bed needs these! They repel pests and attract pollinators. Plant them as a border.",
                "beginner_tip": "French marigolds are the best for pest control. Buy a six-pack of starts from any garden center — they're bulletproof."
            },
            {
                "name": "Cucumbers",
                "emoji": "🥒",
                "category": "VEGETABLE",
                "difficulty": "EASY",
                "days_to_harvest": 55,
                "why_now": "Soil is warm enough for direct sowing. Bush varieties are great for small spaces and containers.",
                "beginner_tip": "Pick them when they're 6-8 inches long. If they turn yellow, you waited too long — but the plant will keep making more."
            },
            {
                "name": "Green Beans (Bush)",
                "emoji": "🫘",
                "category": "VEGETABLE",
                "difficulty": "EASY",
                "days_to_harvest": 50,
                "why_now": "Bush beans are the ultimate beginner crop. Direct sow after last frost (that's now!) and they practically grow themselves.",
                "beginner_tip": "They fix nitrogen in the soil, so plant them where you had heavy feeders last year. Your soil will thank you."
            }
        ],
        "dont_plant_now": [
            {
                "name": "Peas",
                "reason": "Too late — peas are a cool-season crop. Plant them in early March or wait until September for a fall crop."
            },
            {
                "name": "Lettuce / Spinach",
                "reason": "They'll bolt (go to seed) in the summer heat. Wait until September for a fall planting, or grow in deep shade."
            },
            {
                "name": "Garlic",
                "reason": "Garlic needs to be planted in October for a June harvest. Mark your calendar for fall!"
            }
        ],
        "encouragement": "You don't need a perfect garden — you just need to start. Every expert gardener once killed their first plant. Grab some cherry tomatoes and basil, stick them in the ground, water them, and watch the magic happen. 🌱"
    },
    "fallback_confidence": {
        "is_uncertain": False,
        "why_uncertain": "",
        "suggest_human_review": False
    }
}


# =============================================================================
# STREAMING ENDPOINT
# =============================================================================

async def stream_mock_inference():
    """Simulates real-time reasoning trace streaming from MI300X."""

    for idx, step in enumerate(MOCK_REASONING_TRACE):
        update = {
            "type": "reasoning_step",
            "step": step,
            "step_number": idx + 1,
            "total_steps": len(MOCK_REASONING_TRACE)
        }
        yield json.dumps(update).encode() + b'\n'
        await asyncio.sleep(1.0)

    yield json.dumps({
        "type": "complete",
        "data": MOCK_FULL_RESPONSE
    }).encode() + b'\n'


@app.post("/api/sentinel/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """Mock endpoint — streams simulated inference data."""
    return StreamingResponse(
        stream_mock_inference(),
        media_type="application/x-ndjson"
    )


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "mode": "simulated",
        "version": "3.0",
        "hardware": "CPU (Mock Mode)"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
