"""
Geographical and Meteorological Registry for Assam and Northeast India
Contains comprehensive district metadata, coordinates, river basins, localities,
and default secondary predictor relationships.
"""

NE_STATES_DISTRICTS = {
    "Assam": [
        "Bajali", "Baksa", "Barpeta", "Biswanath", "Bongaigaon", "Cachar", "Charaideo",
        "Chirang", "Darrang", "Dhemaji", "Dhubri", "Dibrugarh", "Dima Hasao", "Goalpara",
        "Golaghat", "Hailakandi", "Hojai", "Jorhat", "Kamrup", "Kamrup Metropolitan",
        "Karbi Anglong", "Karimganj", "Kokrajhar", "Lakhimpur", "Majuli", "Morigaon",
        "Nagaon", "Nalbari", "Sivasagar", "Sonitpur", "South Salmara-Mankachar", "Tamulpur",
        "Tinsukia", "Udalguri", "West Karbi Anglong"
    ],
    "Arunachal Pradesh": [
        "Anjaw", "Changlang", "Dibang Valley", "East Kameng", "East Siang", "Itanagar",
        "Kamle", "Kra Daadi", "Kurung Kumey", "Lepa Rada", "Lohit", "Longding",
        "Lower Dibang Valley", "Lower Siang", "Lower Subansiri", "Namsai", "Pakke Kessang",
        "Papum Pare", "Shi Yomi", "Siang", "Tawang", "Tirap", "Upper Siang",
        "Upper Subansiri", "West Kameng", "West Siang"
    ],
    "Meghalaya": [
        "East Garo Hills", "East Jaintia Hills", "East Khasi Hills", "Eastern West Khasi Hills",
        "North Garo Hills", "Ri Bhoi", "South Garo Hills", "South West Garo Hills",
        "South West Khasi Hills", "West Garo Hills", "West Jaintia Hills", "West Khasi Hills"
    ],
    "Mizoram": [
        "Aizawl", "Champhai", "Hnahthial", "Khawzawl", "Kolasib", "Lawngtlai",
        "Lunglei", "Mamit", "Saiha", "Saitual", "Serchhip"
    ],
    "Manipur": [
        "Bishnupur", "Chandel", "Churachandpur", "Imphal East", "Imphal West", "Jiribam",
        "Kakching", "Kamjong", "Kangpokpi", "Noney", "Pherzawl", "Senapati",
        "Tamenglong", "Tengnoupal", "Thoubal", "Ukhrul"
    ],
    "Nagaland": [
        "Chumoukedima", "Dimapur", "Kiphire", "Kohima", "Longleng", "Mokokchung",
        "Mon", "Niuland", "Noklak", "Peren", "Phek", "Shamator",
        "Tseminyu", "Tuensang", "Wokha", "Zunheboto"
    ],
    "Tripura": [
        "Dhalai", "Gomati", "Khowai", "North Tripura", "Sepahijala", "South Tripura",
        "Unakoti", "West Tripura"
    ],
    "Sikkim": [
        "Gangtok", "Gyalshing", "Mangan", "Namchi", "Pakyong", "Soreng"
    ],
    "West Bengal": [
        "Alipurduar", "Cooch Behar", "Darjeeling", "Jalpaiguri", "Kalimpong"
    ]
}

# Primary Assam District Metadata (Coordinates, River Basin, Defaults, Localities)
ASSAM_DISTRICTS_CONFIG = {
    "Hailakandi": {
        "lat": 24.68,
        "lon": 92.56,
        "district_id": 337,
        "river_basin": "Barak Sub-Basin (Dhaleswari & Katakhal Corridor)",
        "subdivision": "Barak Valley",
        "bbox": {"min_lat": 24.20, "max_lat": 24.95, "min_lon": 92.40, "max_lon": 92.75},
        "default_secondary_states": ["Mizoram"],
        "default_secondary_districts": ["Kolasib", "Mamit", "Aizawl"],
        "sectors": [
            {
                "zone_name": "Southern Sector (Mizoram Border & Katlicherra)",
                "coordinates": "24.42° N, 92.58° E",
                "latitude": 24.42,
                "longitude": 92.58,
                "localities": "Katlicherra, Jamira, South Hailakandi, Bilaipur",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Heavy Rain",
                "expected_winds": "💨 Squalls (45 - 55 km/h)",
                "action_suggested": "Take shelter in sturdy structures; avoid open paddy fields and riverbanks.",
                "convective_status": "Severe orographic storm trigger from Mizoram border ridges."
            },
            {
                "zone_name": "Central Sector (Hailakandi HQ & Lala Valley)",
                "coordinates": "24.68° N, 92.56° E",
                "latitude": 24.68,
                "longitude": 92.56,
                "localities": "Hailakandi Town, Lala, Monacherra, DC Office",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Gusty Winds",
                "expected_winds": "💨 Gusty winds (40 - 50 km/h)",
                "action_suggested": "Avoid tin sheds and weak structures during active lightning window.",
                "convective_status": "Active convective cell migration through central river corridor."
            },
            {
                "zone_name": "Northern Sector (Algapur Barak Floodplain)",
                "coordinates": "24.78° N, 92.55° E",
                "latitude": 24.78,
                "longitude": 92.55,
                "localities": "Algapur, Mohanpur, Kalinagar, Barak Bank",
                "alert_level": "Yellow Alert (Be Updated)",
                "alert_color": "Yellow",
                "hazard_phenomenon": "⚡ Moderate Thunderstorm & Lightning",
                "expected_winds": "💨 Gusts (35 - 45 km/h)",
                "action_suggested": "Stay alert for sudden squalls across open floodplains.",
                "convective_status": "Convective spread across open paddy floodplains."
            }
        ]
    },
    "Dibrugarh": {
        "lat": 27.47,
        "lon": 94.91,
        "district_id": 305,
        "river_basin": "Upper Brahmaputra & Burhi Dihing Basin",
        "subdivision": "Upper Assam",
        "bbox": {"min_lat": 27.05, "max_lat": 27.65, "min_lon": 94.70, "max_lon": 95.45},
        "default_secondary_states": ["Arunachal Pradesh", "Assam"],
        "default_secondary_districts": ["Changlang", "Tirap", "East Siang", "Tinsukia"],
        "sectors": [
            {
                "zone_name": "Southern Sector (Naharkatia & Namrup Hills Entry)",
                "coordinates": "27.28° N, 95.33° E",
                "latitude": 27.28,
                "longitude": 95.33,
                "localities": "Naharkatia, Namrup, Joypur Rainforest, Burhi Dihing Bank",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Heavy Showers",
                "expected_winds": "💨 Squalls (40 - 50 km/h)",
                "action_suggested": "Avoid venturing into open plantation tracts and tea garden open grounds.",
                "convective_status": "Convective storm triggers along Patkai foothills and river entry."
            },
            {
                "zone_name": "Central Sector (Dibrugarh City & Moran HQ)",
                "coordinates": "27.47° N, 94.91° E",
                "latitude": 27.47,
                "longitude": 94.91,
                "localities": "Dibrugarh Town, Boiragimoth, Moran, Barbaruah, DC Office",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Gusty Winds",
                "expected_winds": "💨 Gusty winds (35 - 45 km/h)",
                "action_suggested": "Take shelter inside concrete buildings; avoid parking under old trees.",
                "convective_status": "Intense urban-rural heat-moisture convective convergence."
            },
            {
                "zone_name": "Northern Sector (Chabua & Brahmaputra Embankment)",
                "coordinates": "27.52° N, 95.18° E",
                "latitude": 27.52,
                "longitude": 95.18,
                "localities": "Chabua, Rohmoria, Bogibeel Bridge Approach, River Islands",
                "alert_level": "Yellow Alert (Be Updated)",
                "alert_color": "Yellow",
                "hazard_phenomenon": "⚡ Moderate Thunderstorm & Squalls",
                "expected_winds": "💨 Gusts (30 - 40 km/h)",
                "action_suggested": "Suspend boat crossings across Brahmaputra during thunderstorm window.",
                "convective_status": "Wide braided river channel squalls and embankment winds."
            }
        ]
    },
    "Cachar": {
        "lat": 24.83,
        "lon": 92.79,
        "district_id": 336,
        "river_basin": "Central Barak River Basin",
        "subdivision": "Barak Valley",
        "bbox": {"min_lat": 24.40, "max_lat": 25.15, "min_lon": 92.50, "max_lon": 93.30},
        "default_secondary_states": ["Manipur", "Mizoram", "Meghalaya"],
        "default_secondary_districts": ["Pherzawl", "Kolasib", "East Jaintia Hills", "Jiribam"],
        "sectors": [
            {
                "zone_name": "Southern Sector (Dholai & Mizoram Border)",
                "coordinates": "24.60° N, 92.85° E",
                "latitude": 24.60,
                "longitude": 92.85,
                "localities": "Dholai, Kabuganj, Bhagabazar, Lailapur Border",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Heavy Rain",
                "expected_winds": "💨 Squalls (40 - 50 km/h)",
                "action_suggested": "Avoid travel across foothill road links during peak lightning activity.",
                "convective_status": "Upstream hill clouds entering Barak floodplain."
            },
            {
                "zone_name": "Central Sector (Silchar Urban & Lakhipur HQ)",
                "coordinates": "24.83° N, 92.79° E",
                "latitude": 24.83,
                "longitude": 92.79,
                "localities": "Silchar Town, Meherpur, Tarapur, Lakhipur, DC Complex",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Gusty Winds",
                "expected_winds": "💨 Gusts (35 - 45 km/h)",
                "action_suggested": "Avoid tin sheds and open market stalls during sudden downbursts.",
                "convective_status": "Barak river bend moisture accumulation and convective showers."
            },
            {
                "zone_name": "Northern Sector (Borkhola & Jaintia Hills Border)",
                "coordinates": "24.95° N, 92.72° E",
                "latitude": 24.95,
                "longitude": 92.72,
                "localities": "Borkhola, Kalain, Bikrampur, Jatinga Confluence",
                "alert_level": "Yellow Alert (Be Updated)",
                "alert_color": "Yellow",
                "hazard_phenomenon": "⚡ Moderate Thunderstorm & Lightning",
                "expected_winds": "💨 Gusts (35 - 45 km/h)",
                "action_suggested": "Stay alert in orographic foothill zones for sudden lightning discharge.",
                "convective_status": "Jaintia / Barail foothill orographic thunderstorms."
            }
        ]
    },
    "Karimganj": {
        "lat": 24.87,
        "lon": 92.35,
        "district_id": 338,
        "river_basin": "Kushiara & Longai River Basin",
        "subdivision": "Barak Valley",
        "bbox": {"min_lat": 24.25, "max_lat": 25.05, "min_lon": 92.20, "max_lon": 92.65},
        "default_secondary_states": ["Tripura", "Mizoram"],
        "default_secondary_districts": ["North Tripura", "Mamit", "Unakoti"],
        "sectors": [
            {
                "zone_name": "Southern Sector (Patharkandi & Tripura Entry)",
                "coordinates": "24.53° N, 92.33° E",
                "latitude": 24.53,
                "longitude": 92.33,
                "localities": "Patharkandi, Lowairpoa, Bazaricherra, Churaibari",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Gusty Winds",
                "expected_winds": "💨 Squalls (40 - 50 km/h)",
                "action_suggested": "Take shelter in permanent masonry buildings away from high poles.",
                "convective_status": "Longai valley convective entry from Tripura/Mizoram ridges."
            },
            {
                "zone_name": "Central Sector (Karimganj Town & Nilambazar)",
                "coordinates": "24.87° N, 92.35° E",
                "latitude": 24.87,
                "longitude": 92.35,
                "localities": "Karimganj Town, Nilambazar, Settlement Belt, DC Office",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Moderate Rain",
                "expected_winds": "💨 Gusts (35 - 45 km/h)",
                "action_suggested": "Avoid taking shelter under lone trees in open wetland belts.",
                "convective_status": "Kushiara river basin cloud transit and localized thunder cells."
            },
            {
                "zone_name": "Northern Sector (Badarpur & Barak Junction)",
                "coordinates": "24.90° N, 92.58° E",
                "latitude": 24.90,
                "longitude": 92.58,
                "localities": "Badarpur, Bhanga, Deorail, Barak River Confluence",
                "alert_level": "Yellow Alert (Be Updated)",
                "alert_color": "Yellow",
                "hazard_phenomenon": "⚡ Moderate Thunderstorm & Squall",
                "expected_winds": "💨 Gusts (30 - 40 km/h)",
                "action_suggested": "Secure loose structures and stay clear of river junctions.",
                "convective_status": "River junction squalls and wetland convective showers."
            }
        ]
    },
    "Kamrup Metropolitan": {
        "lat": 26.18,
        "lon": 91.75,
        "district_id": 317,
        "river_basin": "Middle Brahmaputra & Meghalaya Plateau Catchment",
        "subdivision": "Lower Assam",
        "bbox": {"min_lat": 26.00, "max_lat": 26.35, "min_lon": 91.50, "max_lon": 92.05},
        "default_secondary_states": ["Meghalaya", "Assam"],
        "default_secondary_districts": ["Ri Bhoi", "East Khasi Hills", "Kamrup"],
        "sectors": [
            {
                "zone_name": "Southern Sector (Meghalaya Foothills & Khanapara)",
                "coordinates": "26.11° N, 91.82° E",
                "latitude": 26.11,
                "longitude": 91.82,
                "localities": "Khanapara, Jorabat, Basistha, Meghalaya Border Gate",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Heavy Downpour",
                "expected_winds": "💨 Squalls (40 - 50 km/h)",
                "action_suggested": "Avoid waterlogged underpasses and exposed foothill roads.",
                "convective_status": "Orographic spillover and flash runoff from Khasi Hills."
            },
            {
                "zone_name": "Central Sector (Guwahati Urban Core & Dispur HQ)",
                "coordinates": "26.18° N, 91.75° E",
                "latitude": 26.18,
                "longitude": 91.75,
                "localities": "Dispur, Panbazar, Paltan Bazar, Ganeshguri, DC Office",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Urban Gusts",
                "expected_winds": "💨 Gusts (35 - 45 km/h)",
                "action_suggested": "Unplug sensitive electrical appliances; avoid standing near billboards.",
                "convective_status": "Urban heat island convective trigger and waterlogging zones."
            },
            {
                "zone_name": "Northern Sector (Brahmaputra Bank & Jalukbari)",
                "coordinates": "26.22° N, 91.68° E",
                "latitude": 26.22,
                "longitude": 91.68,
                "localities": "Jalukbari, Pandu, North Guwahati, Saraighat Approach",
                "alert_level": "Yellow Alert (Be Updated)",
                "alert_color": "Yellow",
                "hazard_phenomenon": "⚡ Moderate Thunderstorm & Riverine Squall",
                "expected_winds": "💨 Gusts (30 - 40 km/h)",
                "action_suggested": "Halt river ferry services during intense squalls.",
                "convective_status": "Brahmaputra river corridor winds and open plain thunder cells."
            }
        ]
    },
    "Jorhat": {
        "lat": 26.75,
        "lon": 94.22,
        "district_id": 310,
        "river_basin": "Central Brahmaputra & Bhogdoi River Basin",
        "subdivision": "Upper Assam",
        "bbox": {"min_lat": 26.50, "max_lat": 27.00, "min_lon": 94.00, "max_lon": 94.50},
        "default_secondary_states": ["Nagaland", "Assam"],
        "default_secondary_districts": ["Mokokchung", "Wokha", "Golaghat", "Sivasagar"],
        "sectors": [
            {
                "zone_name": "Southern Sector (Mariani & Nagaland Foothills)",
                "coordinates": "26.66° N, 94.32° E",
                "latitude": 26.66,
                "longitude": 94.32,
                "localities": "Mariani, Gibbon Sanctuary, Titabar, Naga Foothills",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Squalls",
                "expected_winds": "💨 Squalls (40 - 50 km/h)",
                "action_suggested": "Avoid working in open tea estates and hill footpaths.",
                "convective_status": "Foothill convective trigger along Naga hill ridges."
            },
            {
                "zone_name": "Central Sector (Jorhat Town & Teok HQ)",
                "coordinates": "26.75° N, 94.22° E",
                "latitude": 26.75,
                "longitude": 94.22,
                "localities": "Jorhat Town, Gar-Ali, Teok, Barbheta, DC Office",
                "alert_level": "Yellow Alert (Be Updated)",
                "alert_color": "Yellow",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Moderate Rain",
                "expected_winds": "💨 Gusts (35 - 45 km/h)",
                "action_suggested": "Stay inside concrete buildings during thunder activity.",
                "convective_status": "Bhogdoi river corridor convective movement."
            },
            {
                "zone_name": "Northern Sector (Nimati Ghat & Brahmaputra Corridor)",
                "coordinates": "26.85° N, 94.24° E",
                "latitude": 26.85,
                "longitude": 94.24,
                "localities": "Nimati Ghat, Dhekorgorha, Riverine Bank, Majuli Channel",
                "alert_level": "Yellow Alert (Be Updated)",
                "alert_color": "Yellow",
                "hazard_phenomenon": "⚡ Moderate Thunderstorm & Squall",
                "expected_winds": "💨 Gusts (30 - 40 km/h)",
                "action_suggested": "Secure boat moorings at Nimati Ghat against sudden squall lines.",
                "convective_status": "Open river channel squall line development."
            }
        ]
    },
    "Dhemaji": {
        "lat": 27.48,
        "lon": 94.58,
        "district_id": 304,
        "river_basin": "Northern Brahmaputra & Subansiri-Jiadhal Basin",
        "subdivision": "Upper Assam (North Bank)",
        "bbox": {"min_lat": 27.20, "max_lat": 27.95, "min_lon": 94.30, "max_lon": 95.40},
        "default_secondary_states": ["Arunachal Pradesh", "Assam"],
        "default_secondary_districts": ["East Siang", "Lower Siang", "Upper Subansiri", "Lakhimpur"],
        "sectors": [
            {
                "zone_name": "Northern Sector (Arunachal Foothills & Jonai)",
                "coordinates": "27.83° N, 95.15° E",
                "latitude": 27.83,
                "longitude": 95.15,
                "localities": "Jonai, Dekapam, Simen Chapori, Pasighat Border",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Severe Thunderstorm & Lightning with Heavy Downpour",
                "expected_winds": "💨 Squalls (45 - 55 km/h)",
                "action_suggested": "Avoid crossing hill torrents and riverbeds during lightning strikes.",
                "convective_status": "Intense Himalayan foothill orographic thunderstorms and flash flood trigger."
            },
            {
                "zone_name": "Central Sector (Dhemaji HQ & Jiadhal Basin)",
                "coordinates": "27.48° N, 94.58° E",
                "latitude": 27.48,
                "longitude": 94.58,
                "localities": "Dhemaji Town, Silapathar, Sissiborgaon, DC Complex",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Gusty Winds",
                "expected_winds": "💨 Gusty winds (40 - 50 km/h)",
                "action_suggested": "Stay away from temporary electric wiring and tin structures.",
                "convective_status": "Jiadhal river sandbed and agricultural wetland thunder clouds."
            },
            {
                "zone_name": "Southern Sector (Brahmaputra Floodplain & Bogibeel)",
                "coordinates": "27.35° N, 94.75° E",
                "latitude": 27.35,
                "longitude": 94.75,
                "localities": "Gogamukh, Machkhowa, Bogibeel North Bank",
                "alert_level": "Yellow Alert (Be Updated)",
                "alert_color": "Yellow",
                "hazard_phenomenon": "⚡ Moderate Thunderstorm & Squall",
                "expected_winds": "💨 Gusts (30 - 40 km/h)",
                "action_suggested": "Seek shelter away from open river floodplains.",
                "convective_status": "River embankment squall lines and high humidity moisture traps."
            }
        ]
    }
}

# Generic sector and coordinate defaults generator for any Assam district
DISTRICT_COORDINATES_MAP = {
    "Bajali": (26.52, 91.23),
    "Baksa": (26.68, 91.36),
    "Barpeta": (26.32, 91.00),
    "Biswanath": (26.73, 93.15),
    "Bongaigaon": (26.48, 90.56),
    "Cachar": (24.83, 92.79),
    "Charaideo": (26.96, 94.94),
    "Chirang": (26.54, 90.53),
    "Darrang": (26.45, 92.03),
    "Dhemaji": (27.48, 94.58),
    "Dhubri": (26.02, 89.98),
    "Dibrugarh": (27.47, 94.91),
    "Dima Hasao": (25.18, 93.03),
    "Goalpara": (26.17, 90.62),
    "Golaghat": (26.52, 93.97),
    "Hailakandi": (24.68, 92.56),
    "Hojai": (26.00, 92.86),
    "Jorhat": (26.75, 94.22),
    "Kamrup": (26.32, 91.55),
    "Kamrup Metropolitan": (26.18, 91.75),
    "Karbi Anglong": (26.03, 93.43),
    "Karimganj": (24.87, 92.35),
    "Kokrajhar": (26.40, 90.27),
    "Lakhimpur": (27.23, 94.10),
    "Majuli": (26.95, 94.21),
    "Morigaon": (26.25, 92.34),
    "Nagaon": (26.35, 92.68),
    "Nalbari": (26.44, 91.44),
    "Sivasagar": (26.98, 94.63),
    "Sonitpur": (26.63, 92.79),
    "South Salmara-Mankachar": (25.75, 89.85),
    "Tamulpur": (26.63, 91.57),
    "Tinsukia": (27.50, 95.36),
    "Udalguri": (26.75, 92.10),
    "West Karbi Anglong": (25.85, 92.55)
}

# Catchment and river link relations dictionary
CUSTOM_RIVER_LINKS = {
    # Mizoram to Hailakandi / Barak
    ("Mizoram", "Kolasib", "Hailakandi"): "Direct southern border & Tlawng/Dhaleswari River entry into Hailakandi",
    ("Mizoram", "Mamit", "Hailakandi"): "Southwestern boundary & Tut/Katakhal River catchment draining into Hailakandi",
    ("Mizoram", "Aizawl", "Hailakandi"): "Headwaters of Dhaleswari River catchment draining north",
    ("Mizoram", "Kolasib", "Cachar"): "Southern Barak tributary drainage through Sonai & Dholai",
    ("Mizoram", "Mamit", "Karimganj"): "Longai river headwaters flowing into Karimganj lowlands",
    
    # Arunachal to Dibrugarh / Upper Assam
    ("Arunachal Pradesh", "Changlang", "Dibrugarh"): "Upstream eastern watershed & Burhi Dihing River inflow into Dibrugarh",
    ("Arunachal Pradesh", "Tirap", "Dibrugarh"): "Patkai mountain runoff & Disang/Burhi Dihing tributary network",
    ("Arunachal Pradesh", "East Siang", "Dibrugarh"): "Siang (Brahmaputra main stem) massive upstream discharge corridor",
    ("Arunachal Pradesh", "East Siang", "Dhemaji"): "Direct northern border & Siang river outfall into Dhemaji plains",
    ("Arunachal Pradesh", "Lower Siang", "Dhemaji"): "Gai & Simen river catchment draining from Siang foothills",
    ("Arunachal Pradesh", "Upper Subansiri", "Dhemaji"): "Subansiri mega-river upstream catchment draining into Dhemaji/Lakhimpur",
    ("Arunachal Pradesh", "Papum Pare", "Lakhimpur"): "Ranganadi and Dikrong river catchments directly entering North Lakhimpur",
    ("Arunachal Pradesh", "West Kameng", "Sonitpur"): "Kameng/Jia Bhareli river gorge discharging into Tezpur/Sonitpur",
    
    # Meghalaya to Kamrup / Goalpara / Barak
    ("Meghalaya", "Ri Bhoi", "Kamrup Metropolitan"): "Umtrew / Digaru River catchment directly feeding Guwahati south basin",
    ("Meghalaya", "East Khasi Hills", "Kamrup Metropolitan"): "Cherrapunji-Mawsynram ridge moisture front & Umkhrah-Basistha catchment",
    ("Meghalaya", "East Jaintia Hills", "Cachar"): "Lubha and Jatinga river headwaters discharging into Cachar",
    ("Meghalaya", "West Garo Hills", "Goalpara"): "Krishnai and Dudhnoi river catchments draining north into Goalpara",
    
    # Nagaland to Jorhat / Golaghat / Sivasagar
    ("Nagaland", "Mokokchung", "Jorhat"): "Bhogdoi and Jhanji river mountainous headwaters",
    ("Nagaland", "Wokha", "Golaghat"): "Doyang river hydroelectric catchment draining into Dhansiri/Golaghat",
    ("Nagaland", "Mon", "Sivasagar"): "Dikhow river upper catchment in Nagaland draining into Sivasagar plains",
    ("Nagaland", "Dimapur", "Karbi Anglong"): "Dhansiri river valley sharing contiguous interstate flood corridor",
    
    # Manipur to Cachar / Barak
    ("Manipur", "Jiribam", "Cachar"): "Jiri river boundary confluence joining Barak river at Jirimukh",
    ("Manipur", "Pherzawl", "Cachar"): "Upper Tuivai & Barak main stream headwaters in southern Manipur",
    ("Manipur", "Tamenglong", "Dima Hasao"): "Irang and Barak mountain gorge drainage into Dima Hasao"
}


def get_district_meta(district_name: str) -> dict:
    """Returns metadata, coordinates, and default configuration for an Assam district."""
    if district_name in ASSAM_DISTRICTS_CONFIG:
        return ASSAM_DISTRICTS_CONFIG[district_name]
        
    coords = DISTRICT_COORDINATES_MAP.get(district_name, (26.20, 92.50))
    lat, lon = coords
    
    # Auto-generate intelligent default sectors and predictors
    default_states = ["Assam"]
    default_districts = []
    
    # Assign neighboring defaults based on geographic region
    if lat < 25.5:  # Barak Valley / South Assam
        default_states = ["Mizoram", "Meghalaya"]
        default_districts = ["Kolasib", "Mamit", "East Jaintia Hills"]
        basin = "Barak River Basin"
        subdiv = "Barak Valley"
    elif lon > 94.5:  # Upper Assam / North-East
        default_states = ["Arunachal Pradesh", "Assam"]
        default_districts = ["Changlang", "East Siang", "Tirap"]
        basin = "Upper Brahmaputra Basin"
        subdiv = "Upper Assam"
    elif lon < 91.5:  # Lower Assam / West
        default_states = ["Meghalaya", "West Bengal"]
        default_districts = ["West Garo Hills", "Ri Bhoi", "Alipurduar"]
        basin = "Lower Brahmaputra Basin"
        subdiv = "Lower Assam"
    else:  # Central Assam
        default_states = ["Meghalaya", "Nagaland"]
        default_districts = ["Ri Bhoi", "Wokha"]
        basin = "Central Brahmaputra Basin"
        subdiv = "Central Assam"

    return {
        "lat": lat,
        "lon": lon,
        "district_id": 300,
        "river_basin": basin,
        "subdivision": subdiv,
        "bbox": {"min_lat": round(lat - 0.35, 2), "max_lat": round(lat + 0.35, 2), "min_lon": round(lon - 0.35, 2), "max_lon": round(lon + 0.35, 2)},
        "default_secondary_states": default_states,
        "default_secondary_districts": default_districts,
        "sectors": [
            {
                "zone_name": f"Southern / Upstream Sector ({district_name})",
                "coordinates": f"{lat - 0.15:.2f}° N, {lon:.2f}° E",
                "latitude": round(lat - 0.15, 2),
                "longitude": lon,
                "localities": f"Southern Border Belt, {district_name} South",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Heavy Downpour",
                "expected_winds": "💨 Squalls (40 - 50 km/h)",
                "action_suggested": "Avoid venturing into open agricultural fields or river floodplains.",
                "convective_status": "Upstream convective storm initiation and ridge trigger."
            },
            {
                "zone_name": f"Central HQ Sector ({district_name})",
                "coordinates": f"{lat:.2f}° N, {lon:.2f}° E",
                "latitude": lat,
                "longitude": lon,
                "localities": f"{district_name} Town, DC Office, Central Market",
                "alert_level": "Orange Alert (Be Prepared)",
                "alert_color": "Orange",
                "hazard_phenomenon": "⚡ Thunderstorm & Lightning with Gusty Winds",
                "expected_winds": "💨 Gusts (35 - 45 km/h)",
                "action_suggested": "Take shelter inside sturdy structures; avoid temporary sheds.",
                "convective_status": "Active storm transit corridor over populated administrative belt."
            },
            {
                "zone_name": f"Northern / Riverine Sector ({district_name})",
                "coordinates": f"{lat + 0.15:.2f}° N, {lon:.2f}° E",
                "latitude": round(lat + 0.15, 2),
                "longitude": lon,
                "localities": f"Northern Embankment, Riverine Floodplain",
                "alert_level": "Yellow Alert (Be Updated)",
                "alert_color": "Yellow",
                "hazard_phenomenon": "⚡ Moderate Thunderstorm & Squalls",
                "expected_winds": "💨 Gusts (30 - 40 km/h)",
                "action_suggested": "Stay alert for sudden squall lines and localized water pooling.",
                "convective_status": "Convective spread across open agricultural floodplain."
            }
        ]
    }


def get_river_link(sec_state: str, sec_district: str, target_district: str) -> str:
    """Dynamically determines the hydrological/meteorological link between secondary and primary district."""
    # Check exact match
    if (sec_state, sec_district, target_district) in CUSTOM_RIVER_LINKS:
        return CUSTOM_RIVER_LINKS[(sec_state, sec_district, target_district)]
        
    # Check if from same state
    if sec_state == "Assam":
        return f"Adjoining district tributary watershed & shared {target_district} river corridor"
        
    # Generic intelligent description
    return f"Upstream mountain catchment & moisture advection corridor from {sec_district} ({sec_state}) into {target_district}"
