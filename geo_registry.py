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
    ("Tripura", "North Tripura", "Karimganj"): "Juri and Longai river interstate tributary corridor into Karimganj",
    ("Tripura", "Unakoti", "Karimganj"): "Manu-Singla watershed drainage corridor into southern Karimganj",

    # Arunachal to Upper Assam North/South Bank
    ("Arunachal Pradesh", "Changlang", "Dibrugarh"): "Upstream eastern watershed & Burhi Dihing River inflow into Dibrugarh",
    ("Arunachal Pradesh", "Tirap", "Dibrugarh"): "Patkai mountain runoff & Disang/Burhi Dihing tributary network",
    ("Arunachal Pradesh", "East Siang", "Dibrugarh"): "Siang (Brahmaputra main stem) massive upstream discharge corridor",
    ("Arunachal Pradesh", "East Siang", "Dhemaji"): "Direct northern border & Siang river outfall into Dhemaji plains",
    ("Arunachal Pradesh", "Lower Siang", "Dhemaji"): "Gai & Simen river catchment draining from Siang foothills",
    ("Arunachal Pradesh", "Upper Subansiri", "Dhemaji"): "Subansiri mega-river upstream catchment draining into Dhemaji/Lakhimpur",
    ("Arunachal Pradesh", "Papum Pare", "Lakhimpur"): "Ranganadi and Dikrong river catchments directly entering North Lakhimpur",
    ("Arunachal Pradesh", "Lower Subansiri", "Lakhimpur"): "Subansiri tributary drainage and Gerukamukh foothill discharge",
    ("Arunachal Pradesh", "Lohit", "Tinsukia"): "Lohit river turbulent mountain exit into eastern Tinsukia floodplains",
    ("Arunachal Pradesh", "Namsai", "Tinsukia"): "Noa Dihing river alluvial corridor flowing west into Tinsukia",
    ("Arunachal Pradesh", "Changlang", "Tinsukia"): "Tirap and Burhi Dihing upper watershed mountain runoff",
    ("Arunachal Pradesh", "Tirap", "Charaideo"): "Disang river gorge entry and Patkai range headwaters",
    ("Arunachal Pradesh", "West Kameng", "Sonitpur"): "Kameng/Jia Bhareli river gorge discharging into Tezpur/Sonitpur",
    ("Arunachal Pradesh", "Pakke Kessang", "Sonitpur"): "Pakke and Gabharu foothill catchment entering Sonitpur",
    ("Arunachal Pradesh", "East Kameng", "Biswanath"): "Borgang and Buroi river mountain catchments discharging into Biswanath",
    ("Arunachal Pradesh", "Pakke Kessang", "Biswanath"): "Buroi river headwaters draining southwards into Biswanath plains",
    ("Arunachal Pradesh", "West Kameng", "Darrang"): "Nonai and Mangaldai river foothill drainage basin",
    ("Arunachal Pradesh", "West Kameng", "Udalguri"): "Dhansiri (North) and Bornadi river interstate border catchment",
    ("Arunachal Pradesh", "East Siang", "Majuli"): "Brahmaputra upper trunk channel delivering upstream flood volume into Majuli island",
    ("Arunachal Pradesh", "Lower Subansiri", "Majuli"): "Subansiri channel outfall bounding the northern banks of Majuli",

    # Meghalaya to Central / Lower Assam
    ("Meghalaya", "Ri Bhoi", "Kamrup Metropolitan"): "Umtrew / Digaru River catchment directly feeding Guwahati south basin",
    ("Meghalaya", "East Khasi Hills", "Kamrup Metropolitan"): "Cherrapunji-Mawsynram ridge moisture front & Umkhrah-Basistha catchment",
    ("Meghalaya", "Ri Bhoi", "Kamrup"): "Kulsi river headwaters and southern highland moisture funneling",
    ("Meghalaya", "West Khasi Hills", "Kamrup"): "Boko and Singra river catchment draining north from Khasi hills",
    ("Meghalaya", "West Garo Hills", "Goalpara"): "Krishnai and Dudhnoi river catchments draining north into Goalpara",
    ("Meghalaya", "East Garo Hills", "Goalpara"): "Dudhnoi river upstream forest catchment discharging into Goalpara",
    ("Meghalaya", "South West Garo Hills", "South Salmara-Mankachar"): "Jinjiram river flood basin and border corridor",
    ("Meghalaya", "West Garo Hills", "South Salmara-Mankachar"): "Brahmaputra left bank foothill moisture advection corridor",
    ("Meghalaya", "West Garo Hills", "Dhubri"): "South bank confluence and interstate moisture channel into Dhubri",
    ("Meghalaya", "Ri Bhoi", "Morigaon"): "Killing and Kolong river southern hill drainage into Morigaon",
    ("Meghalaya", "East Khasi Hills", "Morigaon"): "Khasi ridge runoff discharging into southern Morigaon flood basins",
    ("Meghalaya", "Ri Bhoi", "Nagaon"): "Upper Kolong and Barapani river drainage into western Nagaon",
    ("Meghalaya", "West Jaintia Hills", "Hojai"): "Kopili river hydroelectric basin runoff discharging into Hojai valley",
    ("Meghalaya", "West Jaintia Hills", "Dima Hasao"): "Kopili gorge and Kupli river mountain headwaters",
    ("Meghalaya", "East Jaintia Hills", "Cachar"): "Lubha and Jatinga river headwaters discharging into Cachar",
    ("Meghalaya", "Ri Bhoi", "Tamulpur"): "North bank Brahmaputra moisture transfer and southern drainage",
    ("Meghalaya", "Ri Bhoi", "Nalbari"): "Pagladiya and Nona basin regional atmospheric moisture corridor",

    # Nagaland to Upper / Central Assam
    ("Nagaland", "Mokokchung", "Jorhat"): "Bhogdoi and Jhanji river mountainous headwaters",
    ("Nagaland", "Wokha", "Jorhat"): "Doyang river downstream watershed influencing southern Jorhat",
    ("Nagaland", "Wokha", "Golaghat"): "Doyang river hydroelectric catchment draining into Dhansiri/Golaghat",
    ("Nagaland", "Dimapur", "Golaghat"): "Dhansiri river interstate alluvial floodplain corridor",
    ("Nagaland", "Mon", "Sivasagar"): "Dikhow river upper catchment in Nagaland draining into Sivasagar plains",
    ("Nagaland", "Mokokchung", "Sivasagar"): "Jhanji river steep mountain runoff into southwestern Sivasagar",
    ("Nagaland", "Mon", "Charaideo"): "Suffry and Tiru river mountain headwaters entering Charaideo",
    ("Nagaland", "Dimapur", "Karbi Anglong"): "Dhansiri river valley sharing contiguous interstate flood corridor",
    ("Nagaland", "Peren", "Karbi Anglong"): "Diphu and Jamuna river headwaters draining north into Karbi hills",
    ("Nagaland", "Peren", "Dima Hasao"): "Barail range mountain drainage and Jatinga watershed",
    ("Nagaland", "Wokha", "Nagaon"): "Dhansiri-Kolong inter-basin flood transition corridor",
    ("Nagaland", "Peren", "Hojai"): "Jamuna river mountain source discharging into Hojai agricultural valley",

    # Manipur to Cachar / Dima Hasao
    ("Manipur", "Jiribam", "Cachar"): "Jiri river boundary confluence joining Barak river at Jirimukh",
    ("Manipur", "Pherzawl", "Cachar"): "Upper Tuivai & Barak main stream headwaters in southern Manipur",
    ("Manipur", "Tamenglong", "Dima Hasao"): "Irang and Barak mountain gorge drainage into Dima Hasao",

    # West Bengal & Bhutan foothills to Bodoland / Lower Assam
    ("West Bengal", "Alipurduar", "Kokrajhar"): "Sankosh and Saralbhanga river interstate flood plain corridor",
    ("West Bengal", "Cooch Behar", "Kokrajhar"): "Gangadhar and Raidak river lower drainage into western Kokrajhar",
    ("West Bengal", "Cooch Behar", "Dhubri"): "Gangadhar and Brahmaputra entry point from northern Bengal",
    ("West Bengal", "Alipurduar", "Chirang"): "Champamati and Aie river sub-Himalayan foothill drainage",
    ("West Bengal", "Alipurduar", "Barpeta"): "Beki and Manas river downstream braided channel network",
    ("West Bengal", "Alipurduar", "Bajali"): "Pahumara and Kaldia river sub-Himalayan drainage",
    ("West Bengal", "Alipurduar", "Baksa"): "Borolia, Puthimari and Manas tributary runoff corridor"
}

# Complete Hydrological Profiles for all 35 Assam Districts
DISTRICT_HYDROLOGICAL_PROFILE = {
    # 1. Barak River Valley (Southern Assam)
    "Hailakandi": {
        "river_basin": "Barak Sub-Basin (Dhaleswari & Katakhal Corridor)",
        "subdivision": "Barak Valley",
        "catchments": [
            {"state": "Mizoram", "district": "Kolasib"},
            {"state": "Mizoram", "district": "Mamit"},
            {"state": "Mizoram", "district": "Aizawl"}
        ]
    },
    "Cachar": {
        "river_basin": "Central Barak River Basin",
        "subdivision": "Barak Valley",
        "catchments": [
            {"state": "Manipur", "district": "Pherzawl"},
            {"state": "Mizoram", "district": "Kolasib"},
            {"state": "Meghalaya", "district": "East Jaintia Hills"},
            {"state": "Manipur", "district": "Jiribam"}
        ]
    },
    "Karimganj": {
        "river_basin": "Kushiara & Longai River Basin",
        "subdivision": "Barak Valley",
        "catchments": [
            {"state": "Tripura", "district": "North Tripura"},
            {"state": "Mizoram", "district": "Mamit"},
            {"state": "Tripura", "district": "Unakoti"}
        ]
    },

    # 2. Hill Districts
    "Dima Hasao": {
        "river_basin": "Kopili & Diyung Mountain River Basin",
        "subdivision": "Central Assam Hills",
        "catchments": [
            {"state": "Meghalaya", "district": "West Jaintia Hills"},
            {"state": "Manipur", "district": "Tamenglong"},
            {"state": "Nagaland", "district": "Peren"}
        ]
    },
    "Karbi Anglong": {
        "river_basin": "Dhansiri & Kopili Basin",
        "subdivision": "Central Assam Hills",
        "catchments": [
            {"state": "Nagaland", "district": "Dimapur"},
            {"state": "Nagaland", "district": "Peren"},
            {"state": "Meghalaya", "district": "Ri Bhoi"}
        ]
    },
    "West Karbi Anglong": {
        "river_basin": "Upper Kopili & Umkhen River Basin",
        "subdivision": "Central Assam Hills",
        "catchments": [
            {"state": "Meghalaya", "district": "Ri Bhoi"},
            {"state": "Meghalaya", "district": "West Jaintia Hills"}
        ]
    },

    # 3. Upper Assam North Bank
    "Dhemaji": {
        "river_basin": "Northern Brahmaputra & Subansiri-Jiadhal Basin",
        "subdivision": "Upper Assam",
        "catchments": [
            {"state": "Arunachal Pradesh", "district": "East Siang"},
            {"state": "Arunachal Pradesh", "district": "Lower Siang"},
            {"state": "Arunachal Pradesh", "district": "Upper Subansiri"}
        ]
    },
    "Lakhimpur": {
        "river_basin": "Subansiri, Ranganadi & Dikrong Basin",
        "subdivision": "Upper Assam",
        "catchments": [
            {"state": "Arunachal Pradesh", "district": "Papum Pare"},
            {"state": "Arunachal Pradesh", "district": "Lower Subansiri"},
            {"state": "Arunachal Pradesh", "district": "Upper Subansiri"}
        ]
    },

    # 4. Upper Assam South Bank
    "Dibrugarh": {
        "river_basin": "Upper Brahmaputra & Burhi Dihing Basin",
        "subdivision": "Upper Assam",
        "catchments": [
            {"state": "Arunachal Pradesh", "district": "East Siang"},
            {"state": "Arunachal Pradesh", "district": "Changlang"},
            {"state": "Arunachal Pradesh", "district": "Tirap"}
        ]
    },
    "Tinsukia": {
        "river_basin": "Lohit, Dibru & Noa Dihing Basin",
        "subdivision": "Upper Assam",
        "catchments": [
            {"state": "Arunachal Pradesh", "district": "Lohit"},
            {"state": "Arunachal Pradesh", "district": "Namsai"},
            {"state": "Arunachal Pradesh", "district": "Changlang"}
        ]
    },
    "Charaideo": {
        "river_basin": "Disang & Suffry River Corridor",
        "subdivision": "Upper Assam",
        "catchments": [
            {"state": "Arunachal Pradesh", "district": "Tirap"},
            {"state": "Nagaland", "district": "Mon"}
        ]
    },
    "Sivasagar": {
        "river_basin": "Dikhow & Jhanji River Basin",
        "subdivision": "Upper Assam",
        "catchments": [
            {"state": "Nagaland", "district": "Mon"},
            {"state": "Nagaland", "district": "Mokokchung"}
        ]
    },
    "Jorhat": {
        "river_basin": "Bhogdoi & Jhanji River Catchment",
        "subdivision": "Upper Assam",
        "catchments": [
            {"state": "Nagaland", "district": "Mokokchung"},
            {"state": "Nagaland", "district": "Wokha"}
        ]
    },
    "Golaghat": {
        "river_basin": "Dhansiri & Doyang Basin",
        "subdivision": "Upper Assam",
        "catchments": [
            {"state": "Nagaland", "district": "Wokha"},
            {"state": "Nagaland", "district": "Dimapur"}
        ]
    },
    "Majuli": {
        "river_basin": "Brahmaputra-Subansiri River Island Confluence",
        "subdivision": "Upper Assam",
        "catchments": [
            {"state": "Arunachal Pradesh", "district": "East Siang"},
            {"state": "Arunachal Pradesh", "district": "Lower Subansiri"}
        ]
    },

    # 5. Central Assam
    "Nagaon": {
        "river_basin": "Kolong-Kopili Flood Basin",
        "subdivision": "Central Assam",
        "catchments": [
            {"state": "Meghalaya", "district": "Ri Bhoi"},
            {"state": "Nagaland", "district": "Wokha"}
        ]
    },
    "Morigaon": {
        "river_basin": "Killing & Kolong-Brahmaputra Basin",
        "subdivision": "Central Assam",
        "catchments": [
            {"state": "Meghalaya", "district": "Ri Bhoi"},
            {"state": "Meghalaya", "district": "East Khasi Hills"}
        ]
    },
    "Hojai": {
        "river_basin": "Kopili & Jamuna Valley",
        "subdivision": "Central Assam",
        "catchments": [
            {"state": "Meghalaya", "district": "West Jaintia Hills"},
            {"state": "Nagaland", "district": "Peren"}
        ]
    },
    "Sonitpur": {
        "river_basin": "Jia Bhareli (Kameng) & Brahmaputra North Bank",
        "subdivision": "North Assam",
        "catchments": [
            {"state": "Arunachal Pradesh", "district": "West Kameng"},
            {"state": "Arunachal Pradesh", "district": "Pakke Kessang"}
        ]
    },
    "Biswanath": {
        "river_basin": "Borgang & Buroi Sub-Basin",
        "subdivision": "North Assam",
        "catchments": [
            {"state": "Arunachal Pradesh", "district": "East Kameng"},
            {"state": "Arunachal Pradesh", "district": "Pakke Kessang"}
        ]
    },
    "Darrang": {
        "river_basin": "Mangaldai & Nonai North Bank Basin",
        "subdivision": "North Assam",
        "catchments": [
            {"state": "Arunachal Pradesh", "district": "West Kameng"},
            {"state": "Arunachal Pradesh", "district": "Pakke Kessang"}
        ]
    },
    "Udalguri": {
        "river_basin": "Dhansiri (North) & Bornadi Basin",
        "subdivision": "North Assam",
        "catchments": [
            {"state": "Arunachal Pradesh", "district": "West Kameng"}
        ]
    },

    # 6. Lower Assam South Bank
    "Kamrup Metropolitan": {
        "river_basin": "Middle Brahmaputra & Meghalaya Plateau Catchment",
        "subdivision": "Lower Assam",
        "catchments": [
            {"state": "Meghalaya", "district": "Ri Bhoi"},
            {"state": "Meghalaya", "district": "East Khasi Hills"}
        ]
    },
    "Kamrup": {
        "river_basin": "Kulsi & Brahmaputra South Bank Basin",
        "subdivision": "Lower Assam",
        "catchments": [
            {"state": "Meghalaya", "district": "Ri Bhoi"},
            {"state": "Meghalaya", "district": "West Khasi Hills"}
        ]
    },
    "Goalpara": {
        "river_basin": "Krishnai, Dudhnoi & Jinjiram Basin",
        "subdivision": "Lower Assam",
        "catchments": [
            {"state": "Meghalaya", "district": "West Garo Hills"},
            {"state": "Meghalaya", "district": "East Garo Hills"}
        ]
    },
    "South Salmara-Mankachar": {
        "river_basin": "Jinjiram & Brahmaputra Inflow Basin",
        "subdivision": "Lower Assam",
        "catchments": [
            {"state": "Meghalaya", "district": "South West Garo Hills"},
            {"state": "Meghalaya", "district": "West Garo Hills"}
        ]
    },

    # 7. Lower Assam North Bank & Bodoland
    "Nalbari": {
        "river_basin": "Pagladiya & Nona Basin",
        "subdivision": "Lower Assam",
        "catchments": [
            {"state": "Meghalaya", "district": "Ri Bhoi"}
        ]
    },
    "Barpeta": {
        "river_basin": "Beki & Manas River Basin",
        "subdivision": "Lower Assam",
        "catchments": [
            {"state": "West Bengal", "district": "Alipurduar"}
        ]
    },
    "Bajali": {
        "river_basin": "Pahumara & Kaldia Basin",
        "subdivision": "Lower Assam",
        "catchments": [
            {"state": "West Bengal", "district": "Alipurduar"}
        ]
    },
    "Baksa": {
        "river_basin": "Borolia & Puthimari Basin",
        "subdivision": "Bodoland / Lower Assam",
        "catchments": [
            {"state": "West Bengal", "district": "Alipurduar"}
        ]
    },
    "Tamulpur": {
        "river_basin": "Pagladiya & Borolia Foothills",
        "subdivision": "Bodoland / Lower Assam",
        "catchments": [
            {"state": "Meghalaya", "district": "Ri Bhoi"}
        ]
    },
    "Bongaigaon": {
        "river_basin": "Manas & Tunia River Basin",
        "subdivision": "Lower Assam",
        "catchments": [
            {"state": "Meghalaya", "district": "West Garo Hills"}
        ]
    },
    "Chirang": {
        "river_basin": "Aie & Champamati Foothill Basin",
        "subdivision": "Bodoland / Lower Assam",
        "catchments": [
            {"state": "West Bengal", "district": "Alipurduar"}
        ]
    },
    "Kokrajhar": {
        "river_basin": "Sankosh & Saralbhanga Basin",
        "subdivision": "Bodoland / Lower Assam",
        "catchments": [
            {"state": "West Bengal", "district": "Alipurduar"},
            {"state": "West Bengal", "district": "Cooch Behar"}
        ]
    },
    "Dhubri": {
        "river_basin": "Gangadhar, Sankosh & Brahmaputra Entry Basin",
        "subdivision": "Lower Assam",
        "catchments": [
            {"state": "West Bengal", "district": "Cooch Behar"},
            {"state": "Meghalaya", "district": "West Garo Hills"}
        ]
    }
}


def get_upstream_catchments_for_district(district_name: str) -> list:
    """
    Dynamically auto-detects and returns the upstream secondary river catchment 
    districts and states for any given Assam district.
    Returns: list of dicts [{'state': 'Mizoram', 'district': 'Kolasib'}, ...]
    """
    if district_name in DISTRICT_HYDROLOGICAL_PROFILE:
        return list(DISTRICT_HYDROLOGICAL_PROFILE[district_name]["catchments"])
        
    # Check ASSAM_DISTRICTS_CONFIG default
    if district_name in ASSAM_DISTRICTS_CONFIG:
        cfg = ASSAM_DISTRICTS_CONFIG[district_name]
        d_states = cfg.get("default_secondary_states", ["Mizoram"])
        d_dists = cfg.get("default_secondary_districts", [])
        res = []
        for d in d_dists:
            st = d_states[0] if d_states else "Assam"
            for s_name, dlist in NE_STATES_DISTRICTS.items():
                if d in dlist:
                    st = s_name
                    break
            res.append({"state": st, "district": d})
        if res:
            return res

    # General fallback based on coordinate quadrant
    coords = DISTRICT_COORDINATES_MAP.get(district_name, (26.20, 92.50))
    lat, lon = coords
    if lat < 25.5:
        return [
            {"state": "Mizoram", "district": "Kolasib"},
            {"state": "Mizoram", "district": "Mamit"},
            {"state": "Mizoram", "district": "Aizawl"}
        ]
    elif lon > 94.5:
        return [
            {"state": "Arunachal Pradesh", "district": "East Siang"},
            {"state": "Arunachal Pradesh", "district": "Changlang"},
            {"state": "Arunachal Pradesh", "district": "Tirap"}
        ]
    elif lon < 91.5:
        return [
            {"state": "Meghalaya", "district": "West Garo Hills"},
            {"state": "West Bengal", "district": "Alipurduar"}
        ]
    else:
        return [
            {"state": "Meghalaya", "district": "Ri Bhoi"},
            {"state": "Meghalaya", "district": "East Khasi Hills"}
        ]


def get_district_meta(district_name: str) -> dict:
    """Returns metadata, coordinates, river basin, and default configuration for an Assam district."""
    if district_name in ASSAM_DISTRICTS_CONFIG:
        return ASSAM_DISTRICTS_CONFIG[district_name]
        
    coords = DISTRICT_COORDINATES_MAP.get(district_name, (26.20, 92.50))
    lat, lon = coords
    
    # Extract accurate hydrological profile if registered
    if district_name in DISTRICT_HYDROLOGICAL_PROFILE:
        h_prof = DISTRICT_HYDROLOGICAL_PROFILE[district_name]
        basin = h_prof["river_basin"]
        subdiv = h_prof["subdivision"]
        auto_catch = h_prof["catchments"]
        default_states = list({c["state"] for c in auto_catch})
        default_districts = [c["district"] for c in auto_catch]
    else:
        # Fallback based on coordinates
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
