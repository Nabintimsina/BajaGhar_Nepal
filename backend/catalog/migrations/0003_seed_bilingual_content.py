from django.db import migrations, models


def seed_bilingual_content(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Instrument = apps.get_model('catalog', 'Instrument')
    Expert = apps.get_model('catalog', 'Expert')
    LearningContent = apps.get_model('catalog', 'LearningContent')
    Tutorial = apps.get_model('catalog', 'Tutorial')
    TunerConfiguration = apps.get_model('catalog', 'TunerConfiguration')

    category_updates = {
        'string': {
            'name_ne': 'तारवाद्य',
            'description_ne': 'तार तानेर ध्वनि निकालिने वाद्य यन्त्रहरूको समूह।',
        },
        'wind': {
            'name_ne': 'सुषिर वाद्य',
            'description_ne': 'हावा वा श्वास प्रयोग गरेर ध्वनि उत्पन्न गरिने वाद्य यन्त्रहरूको समूह।',
        },
        'percussion': {
            'name_ne': 'तालवाद्य',
            'description_ne': 'ठोकाइ वा प्रहारबाट ध्वनि उत्पन्न हुने वाद्य यन्त्रहरूको समूह।',
        },
    }
    for slug, values in category_updates.items():
        Category.objects.filter(slug=slug).update(**values)

    instrument_updates = {
        'Madal': {
            'name_ne': 'मादल',
            'region_ne': 'मध्य नेपाल',
            'description_ne': 'मादल नेपाली लोकसङ्गीतमा व्यापक रूपमा प्रयोग हुने दुई मुख भएको लोक ढोल हो। यसले गहिरो बेस र चर्को स्वरको सन्तुलित मिश्रण निकाल्छ।',
            'history_ne': 'मादल पुस्तौँदेखि नेपाली लोक परम्पराको केन्द्रमा रहँदै आएको छ, विशेषगरी ग्रामीण समुदायहरूमा। गीत, नृत्य र उत्सवहरूमा यसको व्यापक प्रयोग हुन्छ।',
            'materials_ne': 'यो प्रायः खोक्रो काठबाट बनाइन्छ र दुवै छेउमा जनावरको छाला तन्काएर बाँधिन्छ। ध्वनि गुणस्तर सुधार्न भित्री भागमा कालो सुर ताल्चा पनि लगाइन्छ।',
            'playing_technique_ne': 'मादललाई कम्मर वरिपरि तेर्सो गरी समातेर दुवै हातले बजाइन्छ, जसमा फरक-फरक प्रहार प्रविधिबाट विभिन्न स्वर निकालिन्छन्।',
            'cultural_significance_ne': 'मादल नेपालका सबैभन्दा चिनिने वाद्य यन्त्रहरू मध्ये एक हो, जसले खुसी, उत्सव र सांस्कृतिक एकतालाई जनाउँछ। यो प्रायः चाडपर्व, लोकगीत र सामाजिक जमघटहरूमा प्रयोग हुन्छ।',
        },
        'Sarangi': {
            'name_ne': 'सारङ्गी',
            'region_ne': 'पश्चिम नेपाल',
            'description_ne': 'सारङ्गी एक परम्परागत तान्ने तारवाद्य हो, जसको ध्वनि गहिरो, भावपूर्ण र मानवजस्तै गुणयुक्त हुन्छ। यो प्रायः गायनलाई साथ दिन प्रयोग गरिन्छ।',
            'history_ne': 'सारङ्गीको दक्षिण एसियाली सङ्गीत परम्परामा लामो इतिहास छ र नेपालमा लोक तथा शास्त्रीय सङ्गीतको अभिन्न भाग रहँदै आएको छ। परम्परागत रूपमा यो गन्धर्व समुदायद्वारा बजाइन्छ।',
            'materials_ne': 'यो प्रायः टुन (Toona) जस्ता एकै काठको टुक्राबाट कुँदेर बनाइन्छ र यसमा जनावरको आन्द्राबाट बनेका वा नाइलनका तार तथा छालाले ढाकिएको रेजोनेटर हुन्छ।',
            'playing_technique_ne': 'सारङ्गीलाई धनुष प्रयोग गरेर ठाडो अवस्थामा बजाइन्छ। वादकले तार थिच्न औँलाको टुप्पो होइन, औँलाको छेउ वा नङको भाग प्रयोग गर्दछ, जसले भावनात्मक अभिव्यक्तिको व्यापक दायरा दिन्छ।',
            'cultural_significance_ne': 'सारङ्गी नेपालमा कथावाचन र मौखिक परम्पराको प्रतीक हो। यात्रारत सङ्गीतकारहरूले लोककथा, सामाजिक सन्देश र ऐतिहासिक घटनाहरू सङ्गीतमार्फत सुनाउन यसलाई प्रयोग गर्छन्।',
        },
        'Bansuri': {
            'description': 'The history of the flute is as ancient as human civilization itself, though no written records exist regarding its exact origin. Archaeological excavations in China’s Hunan province uncovered a bone flute called Gudi, made from the bone of a Red-crowned Crane with 5 to 8 holes, considered the earliest specimen of its kind. Similarly, ancient flutes made from mammoth tusks and swan bones were discovered in the Ulm region of Southern Germany. The oldest known flute was found in Divje Babe, Slovenia, crafted from the femur of a young bear. This artifact, featuring 2 and 4 holes, is estimated to be approximately 43,000 years old. While the English Flute evolved in 14th-century Europe, folk instruments like the Pan-Flute were prevalent in South America and Africa.',
            'history': 'The flute has an ancient history and is regarded as one of the oldest melodic instruments in the world. It appears in archaeological findings, classical traditions, and mythological references across civilizations. In Hindu mythology, the flute is closely associated with Lord Krishna, symbolizing divine music and spiritual harmony.',
            'materials': 'A flute is traditionally constructed from a single piece of seasoned bamboo, where one end is closed at the natural node or with a cork. The design includes one mouthpiece and a series of 6 to 7 sound holes. While bamboo remains the preferred material, modern flutes are also crafted from metals like brass, silver, and steel. The length of a flute typically ranges from 15 cm to 60 cm, and its tonal quality depends on the length, thickness, and inner diameter of the bamboo.',
            'playing_technique': 'Playing the flute requires a specific embouchure and precise finger coordination. For a transverse flute, the player blows air across the mouthpiece while using their fingers to manipulate the sound holes. To produce the seven fundamental notes, the holes are either fully covered, half-covered, or left open. Achieving purity in tone requires rigorous and continuous practice. There are three main types of flutes: the side-blown Bamboo Transverse flute, the vertical Blown Pipe (Murli), and the Western or English Flute.',
            'cultural_significance': 'From a religious and cultural perspective, the flute is regarded as a sacred instrument. In Hindu mythology, the era of Dwapar Yuga is closely linked with Lord Krishna, whose divine flute music was said to captivate humans and animals alike. Originally a folk instrument used by shepherds for entertainment while grazing livestock, the flute was elevated to the status of a classical instrument by Pandit Pannalal Ghosh. Later, Pandit Hariprasad Chaurasia gained global fame, establishing it as a pillar of North Indian classical music. In Nepal, legends like Shubha Bahadur Sunam, Prem Otaari, and Gopal Yonzon further popularized its use. Known as Gudi in Hunan, Dvije Bab in Slovenia, and Venu in Sanskrit, it remains a symbol of peace and melody across cultures.',
            'description_ne': 'बाँसुरी नरम, मधुर र शान्त पार्ने ध्वनिका लागि परिचित परम्परागत तिरछो बाँसको बाँसुरी हो। यो नेपाल र दक्षिण एसियाभरि शास्त्रीय तथा लोक सङ्गीतमा व्यापक रूपमा प्रयोग हुन्छ।',
            'history_ne': 'बाँसुरीको इतिहास मानव सभ्यता जत्तिकै पुरानो मानिन्छ, यद्यपि यसको निश्चित सुरुवातको कुनै लिखित तथ्याङ्क छैन । चीनको हुनान प्रान्तमा गरिएको उत्खननमा सारसको हड्डीबाट बनेको ५ देखि ८ वटा प्वाल भएको गुडी नामक बाँसुरी भेटिएको थियो, जुन बाँसुरीको पहिलो नमुना मानिन्छ । यस्तै, जर्मन देशको उल्म क्षेत्रमा हात्तीको दाँत र हाँसको हड्डीबाट बनेका प्राचीन बाँसुरीहरू फेला परेका छन् । विश्वकै सबैभन्दा पुरानो बाँसुरी भने स्लोभेनियाको डिभुजे बेब मा भेटिएको युवा भालुको खुट्टाको हड्डीबाट बनेको २ र ४ वटा प्वाल भएको अवशेषलाई मानिन्छ, जुन करिब ४३ हजार वर्ष पुरानो रहेको छ । १४औँ शताब्दीतिर युरोपमा इङ्ग्लिस फ्लुटको विकास भयो भने दक्षिण अमेरिका र अफ्रिकामा प्यान-फ्लुट जस्ता लोक बाजाहरू प्रचलित थिए ।',
            'materials_ne': 'बाँसुरी मुख्यतया बाँसको एउटै टुक्राबाट बनेको हुन्छ, जसको एउटा आँख्ला (घाट) बन्द गरिएको हुन्छ । बनावटका आधारमा यसमा एउटा मुखछिद्र (फुक्ने प्वाल) र ६ देखि ७ वटा स्वरछिद्र (औँलाले थिच्ने प्वाल) हुन्छन् । बाँसबाहेक हालका दिनमा पित्तल, सिल्भर, र इस्पात (स्टील) जस्ता धातुबाट पनि बाँसुरी बनाउने गरिन्छ । बाँसुरीको लम्बाइ सामान्यतया १५ सेन्टिमिटर (६ इन्च) देखि ६० सेन्टिमिटर (२३.६ इन्च) सम्म हुन्छ । बाँसुरी फुट्नबाट जोगाउन र सुन्दर देखाउन यसमा विभिन्न रंगीन डोरी वा रिवनहरू बाँधिन्छ । यसको स्वर बाँसको लम्बाइ, मोटाइ र भित्री गोलाई (Bore) मा निर्भर गर्दछ ।',
            'playing_technique_ne': 'बाँसुरी बजाउन विशेष मुखाकृति र औँलाहरूको सन्तुलन आवश्यक हुन्छ । तेर्सो बाँसुरी बजाउँदा मुखको प्वालमा ओठ राखेर हावा फुकिन्छ भने औँलाहरूले स्वर छिद्रहरूलाई नियन्त्रण गरिन्छ । यसमा सातवटा मुख्य स्वरहरू (सा, रे, ग, म, प, ध, नि) निकाल्नका लागि औँलाले प्वालहरूलाई पूरै छोप्ने, आधा छोप्ने वा खुल्ला छोड्ने गरिन्छ । गम्भीर र निरन्तर अभ्यासबाट मात्र बाँसुरीको धुनमा शुद्धता ल्याउन सकिन्छ । बाँसुरीका मुख्य तीन प्रकारहरू: तेर्सो फुक्ने (Bamboo Transverse), ठाडो फुक्ने (Murli) र पश्चिमा शैलीको इङ्ग्लिस फ्लुट प्रचलनमा छन् ।',
            'cultural_significance_ne': 'धार्मिक र सांस्कृतिक दृष्टिले बाँसुरीलाई अत्यन्तै पवित्र बाजा मानिन्छ । द्वापर युगमा भगवान श्रीकृष्णले बजाउने बाँसुरीको धुनले सम्पूर्ण मानव र जीवजन्तुलाई मोहित पार्ने पौराणिक मान्यता छ । प्राचीन कालमा गोठालाहरूले भेडाबाख्रा चराउन जाँदा मनोरञ्जनका लागि बजाउने यो लोक बाजालाई शास्त्रीय संगीतमा स्थापित गर्ने श्रेय पण्डित पन्नालाल घोषलाई जान्छ । पछि पण्डित हरिप्रसाद चौरासियाले यसलाई विश्वव्यापी रूपमा शास्त्रीय वाद्य वादनको रूपमा लोकप्रिय बनाए । नेपालमा पनि रेडियो नेपालको स्थापनापछि शुभ बहादुर सुनाम, प्रेम औतारी र गोपाल योञ्जन जस्ता स्रष्टाहरूले बाँसुरीको महत्त्वलाई अझ बढाएका छन् । यसलाई दक्षिण भारतमा पिलाडगोल र संस्कृतमा वेणु भनिन्छ ।',
            'name_ne': 'बाँसुरी',
            'region_ne': 'नेपालभरि',
            'description_ne': 'बाँसुरी नरम, मधुर र शान्त पार्ने ध्वनिका लागि परिचित परम्परागत तिरछो बाँसको बाँसुरी हो। यो नेपाल र दक्षिण एसियाभरि शास्त्रीय तथा लोक सङ्गीतमा व्यापक रूपमा प्रयोग हुन्छ।',
            'history_ne': 'बाँसुरीको प्राचीन उत्पत्ति छ र यो शास्त्रीय ग्रन्थ तथा ऐतिहासिक कलाकृतिहरूमा पनि देखिन्छ। हिन्दू मिथकमा यसलाई भगवान कृष्णसँग जोडिन्छ, जसले दैवी सङ्गीत र आध्यात्मिकतालाई जनाउँछ।',
            'materials_ne': 'यो एकल खोक्रो बाँसको डाँठबाट बनाइन्छ, जुन सावधानीपूर्वक छानिएको र सुकाइएको हुन्छ। यसमा सामान्यतया छ वा सात औँला राख्ने प्वाल र एउटा फुँक्ने प्वाल हुन्छ।',
            'playing_technique_ne': 'बाँसुरी तेर्सो गरी शरीरको छेउमा समातिन्छ र फुँक्ने प्वालमाथि हावा बहाएर स्वर निकालिन्छ, जबकि औँलाको स्थितिबाट पिच नियन्त्रण गरिन्छ।',
            'cultural_significance_ne': 'बाँसुरीको गहिरो आध्यात्मिक र सांस्कृतिक महत्त्व छ, जसलाई भक्ति, ध्यान र शास्त्रीय सङ्गीत परम्परासँग जोडिन्छ। यो धार्मिक प्रस्तुति, लोकसङ्गीत र समकालीन रचनाहरूमा पनि व्यापक रूपमा प्रयोग हुन्छ।',
        },
        'Dhime': {
            'name_ne': 'धिमे',
            'region_ne': 'मध्य नेपाल',
            'description_ne': 'धिमे ठूलो परम्परागत दुई मुखे ढोल हो, जसको गहिरो र गुन्जायमान ध्वनि हुन्छ। यो नेवार सांस्कृतिक सङ्गीतको प्रमुख तालवाद्य हो।',
            'history_ne': 'धिमे शताब्दीयौँदेखि काठमाडौं उपत्यकाका नेवार समुदायमा प्रयोग हुँदै आएको छ र धार्मिक विधि, चाडपर्व तथा शोभायात्राहरूमा यसको महत्वपूर्ण भूमिका रहन्छ।',
            'materials_ne': 'यो खोक्रो काठको शरीरबाट बनाइन्छ र दुवै छेउमा जनावरको छाला तानेर डोरी वा छालाका पट्टाले कसिन्छ।',
            'playing_technique_ne': 'यो वाद्यलाई काँधमा वा कम्मर वरिपरि पट्टा लगाएर बोकिन्छ र हात वा डण्डीले बजाइन्छ, जसबाट दुवै मुखमा तालात्मक ध्वनि उत्पन्न हुन्छ।',
            'cultural_significance_ne': 'धिमे इन्द्रजात्रा र बिस्केट जात्रा जस्ता नेवार पर्वहरूसँग गहिरो रूपमा जोडिएको छ। यसले सामुदायिक पहिचान, परम्परा र कर्मकाण्डीय महत्त्वलाई प्रतिनिधित्व गर्छ।',
        },
    }
    for name, values in instrument_updates.items():
        Instrument.objects.filter(name=name).update(**values)

    expert_updates = {
        'Naresh Prajapati': {
            'name_ne': 'नरेश प्रजापति',
            'expertise_ne': 'धिमे विशेषज्ञ',
            'bio_ne': 'नरेश प्रजापति नेपाली सङ्गीतकार तथा तालवादक हुन्, जसले धिमे र मादल जस्ता परम्परागत वाद्य यन्त्रहरूमा विशेषज्ञता हासिल गरेका छन् र नेपालको सङ्गीतिक विरासतको संरक्षण तथा प्रवर्धनमा समर्पित छन्।',
            'detailed_bio_ne': 'नरेश प्रजापति एक अत्यन्त दक्ष नेपाली सङ्गीतकार, शिक्षक र तालवाद्य विशेषज्ञ हुन्, जससँग परम्परागत तथा समकालीन सङ्गीतमा व्यापक अनुभव छ। त्रिभुवन विश्वविद्यालयबाट ललितकला (सङ्गीत र संस्कृति) मा स्नातकोत्तर सहित, उनले आफ्नो करियर नेपाली सङ्गीत परम्पराको संरक्षण, प्रस्तुति र शिक्षणमा समर्पित गरेका छन्।\n\nउनी मादल, धिमे, तबला, ढोलक, खिन र सितार लगायतका वाद्य यन्त्रहरूमा दक्ष छन्, र भारत, चीन, बङ्गलादेश र डेनमार्क जस्ता देशहरूमा राष्ट्रिय तथा अन्तर्राष्ट्रिय प्रस्तुति दिएका छन्। वर्षौंदेखि उनी संस्कृति निगम (राष्ट्रिय नाचघर) जस्ता प्रतिष्ठित संस्थासँग सक्रिय रूपमा संलग्न छन् र दीपक बज्राचार्य तथा Rhythm Band जस्ता ख्यातिप्राप्त सङ्गीत समूहहरूमा ब्यान्ड सदस्यका रूपमा योगदान दिएका छन्।\n\nप्रस्तुति करियरका साथै उनी शिक्षक तथा गुरु पनि हुन् र आकांक्षी सङ्गीतकारहरूलाई मार्गदर्शन गर्छन्। उनले विभिन्न सांस्कृतिक संस्था र सङ्गीत समाजहरूमा संस्थापक सदस्य, बोर्ड सदस्य र सल्लाहकारका रूपमा महत्वपूर्ण भूमिका निर्वाह गरेका छन्। नेपाली सङ्गीतमा उनको योगदानलाई विभिन्न राष्ट्रिय तथा अन्तर्राष्ट्रिय पुरस्कारहरूले सम्मानित गरिएको छ, जसले उनलाई परम्परागत सङ्गीत क्षेत्रको एक सम्मानित व्यक्तित्व बनाएको छ।',
            'achievements_ne': [
                'विश्व बुक अफ रेकर्ड्स (यूके), लण्डन – २०१९ को सम्मान',
                'क्रिएटिभ रेकर्ड्स नेपाल – २०१९ बाट सम्मानित',
                'अन्तर्राष्ट्रिय मैत्री पुरस्कार, बङ्गलादेश – २०१८',
                'नेपाल संस्कृतिक सङ्घ – २०७५ सालमा सम्मानित',
                'अन्तर्राष्ट्रिय शास्त्रीय नृत्य महोत्सव – २०२४ मा सम्मानित',
                '२०१८ देखि संस्कृति निगम (राष्ट्रिय नाचघर) मा सङ्गीत कलाकार',
                'भोजन गृह प्रा.लि. (२००२–२०१८) का पूर्व सङ्गीतकार',
                'दीपक बज्राचार्य तथा Rhythm Band का ब्यान्ड सदस्य',
                'काठमाडौं म्युजिक अर्केस्ट्रा का संस्थापक सदस्य',
                'Folkmandu Society का संस्थापक सदस्य',
                'नेपाल शास्त्रीय सङ्गीत समाजका बोर्ड सदस्य',
                'भारत, चीन, बङ्गलादेश र डेनमार्कमा अन्तर्राष्ट्रिय प्रस्तुति',
                'काठमाडौं महानगरपालिकाको मेयर कप धिमे प्रतियोगितामा निर्णायक',
                'सामूहिक मादल वादन विश्व रेकर्डका लागि निर्णायक (२०२३)',
                'SAARC सांस्कृतिक महोत्सव (२०१८) मा सहभागी',
                'Umanga र Nepal by Vairabi सहित विभिन्न एल्बममा योगदान'
            ],
        },
        'Shanti Bahadur Rayamajhi': {
            'name_ne': 'शान्ति बहादुर रायमाझी',
            'expertise_ne': 'मादल विशेषज्ञ',
            'bio_ne': 'शान्ति बहादुर रायमाझी २००१–२००२ मा नेपथ्यसँग तालवादकका रूपमा जोडिएका थिए। त्यसपछि उनी शिक्षण करियर र सेसन प्लेइङमा केन्द्रित हुन ब्यान्डबाट अलग भए। २०१० देखि उनी पुनः ब्यान्डसँग आवद्ध छन्। उनको अन्तर्राष्ट्रिय यात्रामा USA, UK, Canada, Australia, New Zealand, Germany, Denmark, South Korea, Japan, Hong Kong, UAE, Qatar, Israel र India समावेश छन्। शान्ति मुख्यतः मादल लगायतका तालवाद्यमा विशेष दक्ष छन्।',
            'detailed_bio_ne': 'शान्ति बहादुर रायमाझी २००१–२००२ मा नेपथ्यसँग तालवादकका रूपमा कार्यरत थिए। पछि उनी शिक्षण करियर र सेसन बजाइमा केन्द्रित हुन ब्यान्डबाट अलग भए। २०१० देखि उनी फेरि ब्यान्डसँग आवद्ध छन्। उनले USA, UK, Canada, Australia, New Zealand, Germany, Denmark, South Korea, Japan, Hong Kong, UAE, Qatar, Israel र India सहित विभिन्न देशहरूमा अन्तर्राष्ट्रिय यात्रा गरेका छन्। उनी विशेषगरी मादल जस्ता नेपाली लोक तालवाद्यमा निपुण छन्।',
            'achievements_ne': [],
        },
    }
    for name, values in expert_updates.items():
        Expert.objects.filter(name=name).update(**values)

    learning_updates = {
        1: {
            'title_ne': 'नेपाली सङ्गीतको परिचय',
            'content_ne': 'नेपाली सङ्गीत विभिन्न जातीय परम्परा, भौगोलिक प्रभाव, र शताब्दीऔँको सांस्कृतिक आदानप्रदानबाट बनेको समृद्ध परम्परा हो।',
        },
        2: {
            'title_ne': 'वाद्य यन्त्र वर्गीकरण',
            'content_ne': 'परम्परागत नेपाली वाद्य यन्त्रहरू ध्वनि उत्पादन गर्ने तरिकाका आधारमा चार मुख्य समूहमा वर्गीकृत गरिन्छन्।',
        },
    }
    for pk, values in learning_updates.items():
        LearningContent.objects.filter(pk=pk).update(**values)

    tutorial_updates = {
        2: {
            'title_ne': 'बाँसुरीको परिचय',
            'description_ne': 'बाँसुरीको आधारभूत अभ्यास र ध्वनि उत्पादनबारे परिचयात्मक भिडियो।',
            'instructor_name_ne': '',
        },
        3: {
            'title_ne': 'धिमे',
            'description_ne': 'धिमेको ताल, पकड र आधारभूत वादन प्रविधि।',
            'instructor_name_ne': 'नरेश प्रजापति',
        },
    }
    for pk, values in tutorial_updates.items():
        Tutorial.objects.filter(pk=pk).update(**values)

    TunerConfiguration.objects.filter(pk=1).update(tuning_name_ne='मानक')


def reverse_seed_bilingual_content(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Instrument = apps.get_model('catalog', 'Instrument')
    Expert = apps.get_model('catalog', 'Expert')
    LearningContent = apps.get_model('catalog', 'LearningContent')
    Tutorial = apps.get_model('catalog', 'Tutorial')
    TunerConfiguration = apps.get_model('catalog', 'TunerConfiguration')

    Category.objects.update(name_ne='', description_ne='')
    Instrument.objects.filter(name='Bansuri').update(
        description='The Bansuri is a traditional transverse bamboo flute known for its soft, melodious, and soothing tones. It is widely used in both classical and folk music across Nepal and South Asia.',
        history='The Bansuri has ancient origins and is mentioned in classical texts and depicted in historical art. It is closely associated with Lord Krishna in Hindu mythology, symbolizing divine music and spirituality.',
        materials='It is made from a single hollow bamboo shaft, carefully selected and seasoned, with six or seven finger holes and one embouchure hole.',
        playing_technique='The instrument is held horizontally to the side, and sound is produced by blowing air across the embouchure hole while controlling pitch through finger placement on the holes.',
        cultural_significance='The Bansuri holds deep spiritual and cultural value, often associated with devotion, meditation, and classical music traditions. It is widely used in religious performances, folk music, and contemporary compositions.',
        name_ne='',
        region_ne='',
        description_ne='',
        history_ne='',
        materials_ne='',
        playing_technique_ne='',
        cultural_significance_ne='',
    )
    Expert.objects.update(
        name_ne='',
        expertise_ne='',
        bio_ne='',
        detailed_bio_ne='',
        achievements_ne=[],
    )
    LearningContent.objects.update(title_ne='', content_ne='')
    Tutorial.objects.update(title_ne='', description_ne='', instructor_name_ne='')
    TunerConfiguration.objects.update(tuning_name_ne='')


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_bilingual_content_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='achievements_ne',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.RunPython(seed_bilingual_content, reverse_seed_bilingual_content),
    ]
