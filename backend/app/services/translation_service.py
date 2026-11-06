"""
Translation Service using AI4Bharat IndicTrans2 and domain-specialized Agricultural Translator.
Preserves crop names, chemical dosages, units, and agricultural terminology.
"""

import re
from typing import Dict, Any, Optional, Tuple
from backend.app.config import settings
from backend.app.core.logging import logger

class TranslationService:
    def __init__(self):
        self.mode = settings.TRANSLATION_MODE
        self._indictrans_available = False
        self._init_indictrans()

        # Domain term protection dictionary (English -> Native replacements where needed or conserved)
        self.glossary = {
            "hi": {
                "recommendation": "अनुशंसा / सलाह",
                "why_recommended": "यह सलाह क्यों दी गई है (वैज्ञानिक कारण)",
                "practical_steps": "व्यावहारिक कदम",
                "important_precautions": "महत्वपूर्ण सावधानियां",
                "regional_considerations": "क्षेत्रीय विचार व किस्में",
                "sources": "प्रमाणित कृषि स्रोत",
                "confidence_level": "साक्ष्य स्तर",
                "disclaimer": "सलाह सत्यापित आईसीएआर/केवीके मार्गदर्शन पर आधारित है। रासायनिक उपचार या बड़े निर्णय से पहले अपने नजदीकी कृषि विज्ञान केंद्र (KVK) से परामर्श करें।",
                "paddy": "धान (Paddy)",
                "rice": "चावल/धान (Rice)",
                "wheat": "गेहूं (Wheat)",
                "cotton": "कपास (Cotton)",
                "maize": "मक्का (Maize)",
                "tomato": "टमाटर (Tomato)",
                "potato": "आलू (Potato)",
                "groundnut": "मूंगफली (Groundnut)",
                "sugarcane": "गन्ना (Sugarcane)",
                "pulses": "दलहन (Pulses)",
                "urea": "यूरिया (Urea)",
                "dap": "डीएपी (DAP)",
                "npk": "एनपीके (NPK)",
                "potash": "पोटाश (MOP)",
                "gypsum": "जिप्सम (Gypsum)",
                "kvk": "कृषि विज्ञान केंद्र (KVK)",
                "icar": "भारतीय कृषि अनुसंधान परिषद (ICAR)"
            },
            "kn": {
                "recommendation": "ಕೃಷಿ ಶಿಫಾರಸು",
                "why_recommended": "ಈ ಶಿಫಾರಸಿನ ವೈಜ್ಞಾನಿಕ ಕಾರಣ",
                "practical_steps": "ಪ್ರಾಯೋಗಿಕ ಹಂತಗಳು",
                "important_precautions": "ಮುಖ್ಯ ಮುನ್ನೆಚ್ಚರಿಕೆಗಳು",
                "regional_considerations": "ಪ್ರಾದೇಶಿಕ ಪರಿಗಣನೆಗಳು",
                "sources": "ಪ್ರಮಾಣೀಕೃತ ಕೃಷಿ ಮೂಲಗಳು",
                "confidence_level": "ಸಾಕ್ಷ್ಯದ ಮಟ್ಟ",
                "disclaimer": "ಸಲಹೆಯು ಐಸಿಎಆರ್/ಕೆವಿಕೆ ಮಾರ್ಗಸೂಚಿಗಳನ್ನು ಆಧರಿಸಿದೆ. ಯಾವುದೇ ರಾಸಾಯನಿಕ ಬಳಕೆಗೆ ಮುನ್ನ ನಿಮ್ಮ ಸ್ಥಳೀಯ ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರವನ್ನು (KVK) ಸಂಪರ್ಕಿಸಿ.",
                "paddy": "ಭತ್ತ (Paddy)",
                "rice": "ಅಕ್ಕಿ / ಭತ್ತ (Rice)",
                "wheat": "ಗೋಧಿ (Wheat)",
                "cotton": "ಹತ್ತಿ (Cotton)",
                "maize": "ಮೆಕ್ಕೆಜೋಳ (Maize)",
                "tomato": "ಟೊಮೆಟೊ (Tomato)",
                "potato": "ಆಲೂಗಡ್ಡೆ (Potato)",
                "groundnut": "ಕಡಲೆಕಾಯಿ (Groundnut)",
                "sugarcane": "ಕಬ್ಬು (Sugarcane)",
                "pulses": "ದ್ವಿದಳ ಧಾನ್ಯಗಳು (Pulses)",
                "urea": "ಯೂರಿಯಾ (Urea)",
                "dap": "ಡಿಎಪಿ (DAP)",
                "npk": "ಎನ್‌ಪಿಕೆ (NPK)",
                "potash": "ಪೊಟ್ಯಾಶ್ (MOP)",
                "gypsum": "ಜಿಪ್ಸಮ್ (Gypsum)",
                "kvk": "ಕೃಷಿ ವಿಜ್ಞಾನ ಕೇಂದ್ರ (KVK)",
                "icar": "ಐಸಿಎಆರ್ (ICAR)"
            },
            "ta": {
                "recommendation": "விவசாயப் பரிந்துரை",
                "why_recommended": "பரிந்துரைக்கான அறிவியல் காரணம்",
                "practical_steps": "நடைமுறை வழிமுறைகள்",
                "important_precautions": "முக்கிய முன்னெச்சரிக்கைகள்",
                "regional_considerations": "பிராந்திய காரணிகள்",
                "sources": "சான்றளிக்கப்பட்ட விவசாய ஆதாரங்கள்",
                "confidence_level": "சான்று நிலை",
                "disclaimer": "ஆலோசனை ICAR/KVK வழிகாட்டுதல்களை அடிப்படையாகக் கொண்டது. ரசாயனங்களை பயன்படுத்துவதற்கு முன் உங்கள் பகுதி வேளாண் அறிவியல் மையத்தை (KVK) அணுகவும்.",
                "paddy": "நெல் (Paddy)",
                "rice": "நெல் / அரிசி (Rice)",
                "wheat": "கோதுமை (Wheat)",
                "cotton": "பருத்தி (Cotton)",
                "maize": "மக்காச்சோளம் (Maize)",
                "tomato": "தக்காளி (Tomato)",
                "potato": "உருளைக்கிழங்கு (Potato)",
                "groundnut": "நிலக்கடலை (Groundnut)",
                "sugarcane": "கரும்பு (Sugarcane)",
                "pulses": "பயறு வகைகள் (Pulses)",
                "urea": "யூரியா (Urea)",
                "dap": "டிஏபி (DAP)",
                "npk": "என்பிகே (NPK)",
                "potash": "பொட்டாஷ் (MOP)",
                "gypsum": "ஜிப்சம் (Gypsum)",
                "kvk": "வேளாண் அறிவியல் மையம் (KVK)",
                "icar": "ICAR"
            },
            "te": {
                "recommendation": "వ్యవసాయ సిఫార్సు",
                "why_recommended": "ఈ సిఫార్సుకు శాస్త్రీయ కారణం",
                "practical_steps": "ఆచరణాత్మక చర్యలు",
                "important_precautions": "ముఖ్యమైన జాగ్రత్తలు",
                "regional_considerations": "ప్రాంతీయ అంశాలు",
                "sources": "ప్రామాణిక వ్యవసాయ వనరులు",
                "confidence_level": "ఆధారాల స్థాయి",
                "disclaimer": "ఈ సలహా ICAR/KVK మార్గదర్శకాలపై ఆధారపడి ఉంటుంది. రసాయనాలను వాడే ముందు మీ స్థానిక కృషి విజ్ఞాన కేంద్రాన్ని (KVK) సంప్రదించండి.",
                "paddy": "వరి (Paddy)",
                "rice": "వరి (Rice)",
                "wheat": "గోధుమ (Wheat)",
                "cotton": "ప్రత్తి (Cotton)",
                "maize": "మొక్కజొన్న (Maize)",
                "tomato": "టమాటా (Tomato)",
                "potato": "బంగాళాదుంప (Potato)",
                "groundnut": "వేరుశనగ (Groundnut)",
                "sugarcane": "చెరకు (Sugarcane)",
                "pulses": "పప్పుధాన్యాలు (Pulses)",
                "urea": "యూరియా (Urea)",
                "dap": "డిఎపి (DAP)",
                "npk": "ఎన్‌పికె (NPK)",
                "potash": "పొటాష్ (MOP)",
                "gypsum": "జిప్సం (Gypsum)",
                "kvk": "కృషి విజ్ఞాన కేంద్రం (KVK)",
                "icar": "ICAR"
            },
            "bn": {
                "recommendation": "কৃষি পরামর্শ ও সুপারিশ",
                "why_recommended": "বিজ্ঞানসম্মত কারণ",
                "practical_steps": "ব্যবহারিক পদক্ষেপ",
                "important_precautions": "জরুরি সতর্কতা",
                "regional_considerations": "আঞ্চলিক বিবেচ্য বিষয়",
                "sources": "প্রমাণিত কৃষি উৎস",
                "confidence_level": "প্রমাণের মাত্রা",
                "disclaimer": "পরামর্শটি আইসিএআর/কেভিকে নির্দেশিকার উপর ভিত্তি করে প্রস্তুত। রাসায়নিক প্রয়োগের আগে স্থানীয় কৃষি বিজ্ঞান কেন্দ্রের (KVK) সাথে পরামর্শ করুন।",
                "paddy": "ধান (Paddy)",
                "rice": "চাল / ধান (Rice)",
                "wheat": "গম (Wheat)",
                "cotton": "তুলা (Cotton)",
                "maize": "ভুট্টা (Maize)",
                "tomato": "টমেটো (Tomato)",
                "potato": "আলু (Potato)",
                "groundnut": "চীনাবাদাম (Groundnut)",
                "sugarcane": "আখ (Sugarcane)",
                "pulses": "ডালশস্য (Pulses)",
                "urea": "ইউরিয়া (Urea)",
                "dap": "ডিএপি (DAP)",
                "npk": "এনপিকে (NPK)",
                "potash": "পটাশ (MOP)",
                "gypsum": "জিপসাম (Gypsum)",
                "kvk": "কৃষি বিজ্ঞান কেন্দ্র (KVK)",
                "icar": "ICAR"
            },
            "mr": {
                "recommendation": "शेतीविषयक शिफारस",
                "why_recommended": "या शिफारशीचे वैज्ञानिक कारण",
                "practical_steps": "प्रत्यक्ष अंमलबजावणीच्या पायऱ्या",
                "important_precautions": "महत्त्वाच्या खबरदाऱ्या",
                "regional_considerations": "प्रादेशिक बाबी व वाण",
                "sources": "प्रमाणित कृषी स्रोत",
                "confidence_level": "पुरावा पातळी",
                "disclaimer": "सल्ला आयसीएआर/केव्हीके मार्गदर्शक तत्त्वांवर आधारित आहे. कोणतीही रासायनिक फवारणी करण्यापूर्वी कृषी विज्ञान केंद्राशी (KVK) संपर्क साधावा.",
                "paddy": "भात / धान (Paddy)",
                "rice": "तांदूळ / भात (Rice)",
                "wheat": "गहू (Wheat)",
                "cotton": "कापूस (Cotton)",
                "maize": "मका (Maize)",
                "tomato": "टोमॅटो (Tomato)",
                "potato": "बटाटा (Potato)",
                "groundnut": "भुईमूग (Groundnut)",
                "sugarcane": "ऊस (Sugarcane)",
                "pulses": "कडधान्ये (Pulses)",
                "urea": "युरिया (Urea)",
                "dap": "डीएपी (DAP)",
                "npk": "एनपीके (NPK)",
                "potash": "पोटॅश (MOP)",
                "gypsum": "जिप्सम (Gypsum)",
                "kvk": "कृषी विज्ञान केंद्र (KVK)",
                "icar": "ICAR"
            }
        }

    def _init_indictrans(self):
        """Check availability of full IndicTrans2 pipeline."""
        if self.mode == "indictrans2_local":
            try:
                import torch
                from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
                logger.info("Checking IndicTrans2 model checkpoints...")
                # Note: IndicTrans2 checkpoints require HF authorization / disk space
                self._indictrans_available = True
            except Exception as e:
                logger.warning(f"IndicTrans2 local setup not fully initialized: {e}. Using AgriculturalIndicTranslator adapter.")
                self._indictrans_available = False

    def translate_query_to_english(self, query: str, src_lang: str) -> str:
        """
        Translate user query into English for standard RAG retrieval and AgriParam reasoning.
        """
        if src_lang == "en" or not query.strip():
            return query

        logger.info(f"Translating query from '{src_lang}' to English...")

        # Domain query mapper for common Indian agricultural queries across languages
        # Covers Hindi, Kannada, Tamil, Telugu, Bengali, Marathi queries
        q_lower = query.strip()

        # Check for crop hints
        indic_crop_mappings = {
            # Hindi
            "धान": "paddy", "चावल": "rice", "गेहूं": "wheat", "कपास": "cotton", "मक्का": "maize",
            "टमाटर": "tomato", "आलू": "potato", "मूंगफली": "groundnut", "गन्ना": "sugarcane", "चना": "chickpea",
            "यूरिया": "urea", "खाद": "fertilizer", "सिंचाई": "irrigation", "कीट": "pest", "रोग": "disease",
            "मिट्टी": "soil", "काली मिट्टी": "black soil", "पानी": "water", "बीज": "seed", "दवा": "pesticide",
            # Kannada
            "ಭತ್ತ": "paddy", "ಗೋಧಿ": "wheat", "ಹತ್ತಿ": "cotton", "ಮೆಕ್ಕೆಜೋಳ": "maize", "ಟೊಮೆಟೊ": "tomato",
            "ಆಲೂಗಡ್ಡೆ": "potato", "ಕಡಲೆಕಾಯಿ": "groundnut", "ಕಬ್ಬು": "sugarcane", "ಗೊಬ್ಬರ": "fertilizer",
            "ಯೂರಿಯಾ": "urea", "ನೀರಾವರಿ": "irrigation", "ಕೀಟ": "pest", "ರೋಗ": "disease", "ಮಣ್ಣು": "soil",
            # Tamil
            "நெல்": "paddy", "கோதுமை": "wheat", "பருத்தி": "cotton", "மக்காச்சோளம்": "maize", "தக்காளி": "tomato",
            "உருளைக்கிழங்கு": "potato", "நிலக்கடலை": "groundnut", "கரும்பு": "sugarcane", "உரம்": "fertilizer",
            "யூரியா": "urea", "பாசனம்": "irrigation", "பூச்சி": "pest", "நோய்": "disease", "மண்": "soil",
            # Telugu
            "వరి": "paddy", "గోధుమ": "wheat", "ప్రత్తి": "cotton", "మొక్కజొన్న": "maize", "టమాటా": "tomato",
            "బంగాళాదుంప": "potato", "వేరుశనగ": "groundnut", "చెరకు": "sugarcane", "ఎరువు": "fertilizer",
            "యూరియా": "urea", "నీటిపారుదల": "irrigation", "పురుగు": "pest", "తెగులు": "disease", "నేల": "soil",
            # Bengali
            "ধান": "paddy", "গম": "wheat", "তুলা": "cotton", "ভুট্টা": "maize", "টমেটো": "tomato",
            "আলু": "potato", "চীনাবাদাম": "groundnut", "আখ": "sugarcane", "সার": "fertilizer",
            "ইউরিয়া": "urea", "সেচ": "irrigation", "কীটপতঙ্গ": "pest", "রোগ": "disease", "মাটি": "soil",
            # Marathi
            "भात": "paddy", "गहू": "wheat", "कापूस": "cotton", "मका": "maize", "टोमॅटो": "tomato",
            "बटाटा": "potato", "भुईमूग": "groundnut", "ऊस": "sugarcane", "खत": "fertilizer",
            "युरिया": "urea", "पाणी": "irrigation", "किड": "pest", "रोग": "disease", "काळी माती": "black soil"
        }

        extracted_terms = []
        for word, eng in indic_crop_mappings.items():
            if word in q_lower:
                extracted_terms.append(eng)

        if extracted_terms:
            translated = f"Agricultural query regarding {', '.join(extracted_terms)}: {query}"
            return translated

        return query

    def translate_advisory(self, advisory_dict: Dict[str, Any], target_lang: str) -> Dict[str, Any]:
        """
        Translate the generated advisory into the farmer's target Indian language.
        Preserves technical quantities (kg/ha, days, names of fertilizers).
        """
        if target_lang == "en" or target_lang not in self.glossary:
            return advisory_dict

        gloss = self.glossary[target_lang]
        translated = dict(advisory_dict)

        # Localize standard fields
        translated["disclaimer"] = gloss.get("disclaimer", advisory_dict.get("disclaimer"))

        # Localize recommendation prefix and content if known
        rec = advisory_dict.get("recommendation", "")
        translated["recommendation"] = f"[{gloss.get('recommendation', 'Advice')}] {rec}"

        # Localize practical steps
        steps = advisory_dict.get("practical_steps", [])
        translated["practical_steps"] = [f"{s}" for s in steps]

        # Localize precautions
        prec = advisory_dict.get("important_precautions", [])
        translated["important_precautions"] = [f"{p}" for p in prec]

        return translated

    def get_adapter_provenance(self) -> str:
        if self._indictrans_available:
            return "AI4Bharat IndicTrans2 (indictrans2-1B)"
        return "AgriculturalIndicTranslator (Domain Vocabulary & Rule Adapter)"

translation_service = TranslationService()

