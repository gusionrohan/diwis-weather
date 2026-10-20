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

    # North Bank Intra-Assam & Sub-Himalayan Bhutan Corridors
    ("Assam", "Baksa", "Nalbari"): "Pagladiya and Nona river upper reaches draining directly from Bhutan border through Baksa into Nalbari plains",
    ("Assam", "Tamulpur", "Nalbari"): "Borolia and Pagladiya foothill corridor delivering upstream flash runoff into northern Nalbari",
    ("West Bengal", "Alipurduar", "Nalbari"): "Sub-Himalayan Dooars & Indo-Bhutan border rainfall index for north-bank river systems",
    ("Assam", "Baksa", "Barpeta"): "Upper Beki and Pahumara river basin draining southwards into Barpeta",
    ("Assam", "Chirang", "Barpeta"): "Upper Manas river braided channel corridor discharging into western Barpeta",
    ("Assam", "Baksa", "Bajali"): "Pahumara and Kaldia river upper catchment discharging south into Bajali",
    ("Assam", "Chirang", "Bongaigaon"): "Aie and Manas upper river basin flowing directly south from Bhutan border through Chirang into Bongaigaon",
    ("West Bengal", "Alipurduar", "Bongaigaon"): "Sub-Himalayan Dooars foothill drainage influencing northern tributary inflows into Bongaigaon",
    ("Assam", "Baksa", "Tamulpur"): "Contiguous Bhutan foothill hydrometeorological corridor",
    ("Arunachal Pradesh", "West Kameng", "Tamulpur"): "Eastern Himalayan mountain watershed bordering north-eastern Bodoland",
    ("Arunachal Pradesh", "West Kameng", "Baksa"): "Eastern Himalayan foothills bordering upper Baksa/Bhutan drainage divide",
    ("Assam", "Kokrajhar", "Chirang"): "Champamati and Saralbhanga contiguous river corridor",

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

    # 7. Lower Assam North Bank & Bodoland (Bhutan Himalayan Foothills Catchment)
    "Nalbari": {
        "river_basin": "Pagladiya, Nona & Borolia Basin (Bhutan Foothills)",
        "subdivision": "Lower Assam North Bank",
        "catchments": [
            {"state": "Assam", "district": "Baksa"},
            {"state": "Assam", "district": "Tamulpur"},
            {"state": "West Bengal", "district": "Alipurduar"}
        ]
    },
    "Barpeta": {
        "river_basin": "Beki & Manas River Basin (Bhutan Catchment)",
        "subdivision": "Lower Assam North Bank",
        "catchments": [
            {"state": "Assam", "district": "Baksa"},
            {"state": "Assam", "district": "Chirang"},
            {"state": "West Bengal", "district": "Alipurduar"}
        ]
    },
    "Bajali": {
        "river_basin": "Pahumara & Kaldia Basin (Bhutan Foothills)",
        "subdivision": "Lower Assam North Bank",
        "catchments": [
            {"state": "Assam", "district": "Baksa"},
            {"state": "West Bengal", "district": "Alipurduar"}
        ]
    },
    "Baksa": {
        "river_basin": "Borolia, Pagladiya & Puthimari Basin (Indo-Bhutan Border)",
        "subdivision": "Bodoland / Lower Assam",
        "catchments": [
            {"state": "West Bengal", "district": "Alipurduar"},
            {"state": "Arunachal Pradesh", "district": "West Kameng"}
        ]
    },
    "Tamulpur": {
        "river_basin": "Pagladiya & Borolia Foothills (Indo-Bhutan Border)",
        "subdivision": "Bodoland / Lower Assam",
        "catchments": [
            {"state": "Assam", "district": "Baksa"},
            {"state": "Arunachal Pradesh", "district": "West Kameng"},
            {"state": "West Bengal", "district": "Alipurduar"}
        ]
    },
    "Bongaigaon": {
        "river_basin": "Aie, Manas & Tunia River Basin (North Bank)",
        "subdivision": "Lower Assam North Bank",
        "catchments": [
            {"state": "Assam", "district": "Chirang"},
            {"state": "West Bengal", "district": "Alipurduar"}
        ]
    },
    "Chirang": {
        "river_basin": "Aie & Champamati Foothill Basin (Indo-Bhutan Border)",
        "subdivision": "Bodoland / Lower Assam",
        "catchments": [
            {"state": "West Bengal", "district": "Alipurduar"},
            {"state": "Assam", "district": "Kokrajhar"}
        ]
    },
    "Kokrajhar": {
        "river_basin": "Sankosh & Saralbhanga Basin (Indo-Bhutan Border)",
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
            {"state": "West Bengal", "district": "Alipurduar"},
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
    elif lat > 26.2 and lon < 92.5:  # North Bank Lower Assam / Bodoland
        return [
            {"state": "Assam", "district": "Baksa"},
            {"state": "West Bengal", "district": "Alipurduar"}
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


ASSAM_DISTRICTS_SECTORS_REGISTRY = {
    "Bajali": [
        {
            "zone_name": "Northern Sector (Sarupeta / Pahumara Foothills)",
            "coordinates": "26.62° N, 91.20° E",
            "latitude": 26.62,
            "longitude": 91.20,
            "localities": "Sarupeta, Bhawanipur, Pahumara River Corridor",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Pathsala HQ & Administrative Belt)",
            "coordinates": "26.52° N, 91.23° E",
            "latitude": 26.52,
            "longitude": 91.23,
            "localities": "Pathsala Town, DC Office, NH-27 Corridor, Muguria",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Baghmara & Agricultural Plains)",
            "coordinates": "26.42° N, 91.25° E",
            "latitude": 26.42,
            "longitude": 91.25,
            "localities": "Baghmara, Choukhuti, Simla Riverine Plains",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Baksa": [
        {
            "zone_name": "Northern Sector (Subankhata Bhutan Foothills & Pagladiya Upper Reach)",
            "coordinates": "26.82° N, 91.38° E",
            "latitude": 26.82,
            "longitude": 91.38,
            "localities": "Subankhata, Kumarikata, Bhutan Gate, Bogamati",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Mushalpur HQ & Barama Corridor)",
            "coordinates": "26.68° N, 91.36° E",
            "latitude": 26.68,
            "longitude": 91.36,
            "localities": "Mushalpur Town, DC Office, Barama, Baska Forest Corridor",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Western Sector (Jalah & Manas River Basin)",
            "coordinates": "26.58° N, 91.15° E",
            "latitude": 26.58,
            "longitude": 91.15,
            "localities": "Jalah, Salbari, Manas National Park Entrance, Beki Outfall",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Barpeta": [
        {
            "zone_name": "Northern Sector (Barnagar & Sorbhog Beki Corridor)",
            "coordinates": "26.48° N, 90.95° E",
            "latitude": 26.48,
            "longitude": 90.95,
            "localities": "Barnagar, Sorbhog, Manas & Beki River Corridor",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Barpeta Town & Sarthebari Bell-Metal Core)",
            "coordinates": "26.32° N, 91.00° E",
            "latitude": 26.32,
            "longitude": 91.00,
            "localities": "Barpeta Town, Sarthebari, Howly, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Baghbor & Brahmaputra Active Floodplain)",
            "coordinates": "26.18° N, 90.90° E",
            "latitude": 26.18,
            "longitude": 90.90,
            "localities": "Baghbor, Chenga, Mandia, Brahmaputra Char Belt",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Biswanath": [
        {
            "zone_name": "Northern Sector (Behali & Borgang Arunachal Foothills)",
            "coordinates": "26.88° N, 93.25° E",
            "latitude": 26.88,
            "longitude": 93.25,
            "localities": "Behali, Borgang River Entry, Arunachal Border Ridges",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Biswanath Chariali HQ & Commercial Belt)",
            "coordinates": "26.73° N, 93.15° E",
            "latitude": 26.73,
            "longitude": 93.15,
            "localities": "Biswanath Chariali Town, DC Office, Pavoi, NH-15",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Eastern Sector (Gohpur & Biswanath Ghat Brahmaputra Bank)",
            "coordinates": "26.65° N, 93.45° E",
            "latitude": 26.65,
            "longitude": 93.45,
            "localities": "Gohpur, Helem, Biswanath Ghat, Buroi Outfall",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Bongaigaon": [
        {
            "zone_name": "Northern Sector (Dangtol & Aie River Corridor)",
            "coordinates": "26.58° N, 90.58° E",
            "latitude": 26.58,
            "longitude": 90.58,
            "localities": "Dangtol, Aie Riverbank, Chirang Border, Dhaligaon Link",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Bongaigaon City & Refinery Industrial Core)",
            "coordinates": "26.48° N, 90.56° E",
            "latitude": 26.48,
            "longitude": 90.56,
            "localities": "Bongaigaon City, New Bongaigaon, DC Office, Station Belt",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Abhayapuri & Boitamari Tunia Basin)",
            "coordinates": "26.35° N, 90.62° E",
            "latitude": 26.35,
            "longitude": 90.62,
            "localities": "Abhayapuri, Boitamari, Srijangram, Tunia River Basin",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Cachar": [
        {
            "zone_name": "Southern Sector (Sonai Valley & Mizoram Border)",
            "coordinates": "24.62° N, 92.90° E",
            "latitude": 24.62,
            "longitude": 92.90,
            "localities": "Sonai, Dholai, Kabuganj, Mizoram Border Foothills",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Silchar Urban & Barak Basin)",
            "coordinates": "24.83° N, 92.79° E",
            "latitude": 24.83,
            "longitude": 92.79,
            "localities": "Silchar City, Tarapur, Rangirkhari, DC Office Complex",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Northern Sector (Udharbond & Jatinga Entry)",
            "coordinates": "24.95° N, 92.88° E",
            "latitude": 24.95,
            "longitude": 92.88,
            "localities": "Udharbond, Katigorah, Kumbhirgram, Jatinga Outfall",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Charaideo": [
        {
            "zone_name": "Northern Sector (Mahmora & Disang Plains)",
            "coordinates": "27.08° N, 94.88° E",
            "latitude": 27.08,
            "longitude": 94.88,
            "localities": "Mahmora, Moran Border, Disang Alluvial Floodplain",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Sonari HQ & Historic Charaideo Belt)",
            "coordinates": "26.96° N, 94.94° E",
            "latitude": 26.96,
            "longitude": 94.94,
            "localities": "Sonari Town, DC Office, Charaideo Maidams, Disang Bank",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Sapekhati & Patkai Border Ridges)",
            "coordinates": "26.85° N, 95.12° E",
            "latitude": 26.85,
            "longitude": 95.12,
            "localities": "Sapekhati, Borhat, Tirap & Nagaland Foothill Border",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Chirang": [
        {
            "zone_name": "Northern Sector (Runikhata & Indo-Bhutan Foothills)",
            "coordinates": "26.70° N, 90.55° E",
            "latitude": 26.70,
            "longitude": 90.55,
            "localities": "Runikhata, Champamati Upper Watershed, Bhutan Border",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Kajalgaon HQ & Refinery Corridor)",
            "coordinates": "26.54° N, 90.53° E",
            "latitude": 26.54,
            "longitude": 90.53,
            "localities": "Kajalgaon HQ, Dhaligaon, Sidli, Chapaguri",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Eastern Sector (Bijni & Aie River Basin)",
            "coordinates": "26.50° N, 90.68° E",
            "latitude": 26.50,
            "longitude": 90.68,
            "localities": "Bijni Town, Aie River Valley, NH-27 Corridor",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Darrang": [
        {
            "zone_name": "Northern Sector (Patharighat & Nonai River Basin)",
            "coordinates": "26.58° N, 91.95° E",
            "latitude": 26.58,
            "longitude": 91.95,
            "localities": "Patharighat, Nonai Basin, Bhutan/Udalguri Foothills",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Mangaldai HQ & Sipajhar Corridor)",
            "coordinates": "26.45° N, 92.03° E",
            "latitude": 26.45,
            "longitude": 92.03,
            "localities": "Mangaldai Town, Sipajhar, DC Office, NH-15",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Kharupetia & Dalgaon Brahmaputra Chars)",
            "coordinates": "26.35° N, 92.15° E",
            "latitude": 26.35,
            "longitude": 92.15,
            "localities": "Kharupetia, Dalgaon, Brahmaputra Riverine Island Belt",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Dhemaji": [
        {
            "zone_name": "Northern Sector (Jonai & Siang River Entry)",
            "coordinates": "27.78° N, 95.15° E",
            "latitude": 27.78,
            "longitude": 95.15,
            "localities": "Jonai, Dekapam, Simen Chapori, Arunachal Border",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Dhemaji HQ & Jiadhal Basin)",
            "coordinates": "27.48° N, 94.58° E",
            "latitude": 27.48,
            "longitude": 94.58,
            "localities": "Dhemaji Town, DC Office, Jiadhal Basin, Gogamukh",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Sissiborgaon & Bogibeel North Bank)",
            "coordinates": "27.35° N, 94.75° E",
            "latitude": 27.35,
            "longitude": 94.75,
            "localities": "Sissiborgaon, Silapathar, Bogibeel Approach, Brahmaputra Bank",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Dhubri": [
        {
            "zone_name": "Northern Sector (Golakganj & Agomoni Gangadhar Basin)",
            "coordinates": "26.15° N, 89.92° E",
            "latitude": 26.15,
            "longitude": 89.92,
            "localities": "Golakganj, Agomoni, Gangadhar River Interstate Basin",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Dhubri Port & Gauripur Historical Belt)",
            "coordinates": "26.02° N, 89.98° E",
            "latitude": 26.02,
            "longitude": 89.98,
            "localities": "Dhubri Town, Gauripur, Brahmaputra Inland Port, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Eastern Sector (Bilasipara & Chapar Riverine Plains)",
            "coordinates": "26.22° N, 90.23° E",
            "latitude": 26.22,
            "longitude": 90.23,
            "localities": "Bilasipara, Chapar, Tipkai River Basin, Mahamaya",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Dibrugarh": [
        {
            "zone_name": "Southern Sector (Naharkatia & Namrup Hills Entry)",
            "coordinates": "27.28° N, 95.33° E",
            "latitude": 27.28,
            "longitude": 95.33,
            "localities": "Naharkatia, Namrup, Joypur Rainforest, Burhi Dihing Bank",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Dibrugarh City & Moran HQ)",
            "coordinates": "27.47° N, 94.91° E",
            "latitude": 27.47,
            "longitude": 94.91,
            "localities": "Dibrugarh Town, Boiragimoth, Moran, Barbaruah, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Northern Sector (Chabua & Brahmaputra Embankment)",
            "coordinates": "27.52° N, 95.18° E",
            "latitude": 27.52,
            "longitude": 95.18,
            "localities": "Chabua, Rohmoria, Bogibeel Bridge Approach, River Islands",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Dima Hasao": [
        {
            "zone_name": "Northern Sector (Maibang & Diyung Mountain River Valley)",
            "coordinates": "25.30° N, 93.15° E",
            "latitude": 25.30,
            "longitude": 93.15,
            "localities": "Maibang, Diyung River Gorge, Langting, Dihangi",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Haflong Hill Station & Mahur Ridge HQ)",
            "coordinates": "25.18° N, 93.03° E",
            "latitude": 25.18,
            "longitude": 93.03,
            "localities": "Haflong Town, Mahur, Jatinga Bird Ridge, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Umrangso Hydel Basin & Harangajao Valley)",
            "coordinates": "25.50° N, 92.75° E",
            "latitude": 25.50,
            "longitude": 92.75,
            "localities": "Umrangso, Kopili Dam Catchment, Harangajao Valley",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Goalpara": [
        {
            "zone_name": "Northern Sector (Lakhipur & Jaleswar Brahmaputra Bank)",
            "coordinates": "26.20° N, 90.40° E",
            "latitude": 26.20,
            "longitude": 90.40,
            "localities": "Lakhipur, Jaleswar, Brahmaputra Northern Floodplain",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Goalpara Town & Urpod Beel Basin)",
            "coordinates": "26.17° N, 90.62° E",
            "latitude": 26.17,
            "longitude": 90.62,
            "localities": "Goalpara Town, Balijana, Urpod Beel Wetland, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Dudhnoi & Rongjuli Meghalaya Border)",
            "coordinates": "25.98° N, 90.72° E",
            "latitude": 25.98,
            "longitude": 90.72,
            "localities": "Dudhnoi, Matia, Rongjuli, Krishnai River Foothills",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Golaghat": [
        {
            "zone_name": "Northern Sector (Bokakhat & Kaziranga Floodplain Corridor)",
            "coordinates": "26.62° N, 93.60° E",
            "latitude": 26.62,
            "longitude": 93.60,
            "localities": "Bokakhat, Kohora, Kaziranga National Park Entrance",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Golaghat Town & Dergaon Dhansiri Basin)",
            "coordinates": "26.52° N, 93.97° E",
            "latitude": 26.52,
            "longitude": 93.97,
            "localities": "Golaghat Town, Dergaon, Dhansiri Valley, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Sarupathar & Morangi Nagaland Border)",
            "coordinates": "26.18° N, 93.82° E",
            "latitude": 26.18,
            "longitude": 93.82,
            "localities": "Sarupathar, Uriamghat, Merapani, Doyang River Entry",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Hailakandi": [
        {
            "zone_name": "Southern Sector (Mizoram Border & Katlicherra)",
            "coordinates": "24.42° N, 92.58° E",
            "latitude": 24.42,
            "longitude": 92.58,
            "localities": "Katlicherra, Jamira, South Hailakandi, Bilaipur",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Hailakandi HQ & Lala Valley)",
            "coordinates": "24.68° N, 92.56° E",
            "latitude": 24.68,
            "longitude": 92.56,
            "localities": "Hailakandi Town, Lala, Monacherra, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Northern Sector (Algapur Barak Floodplain)",
            "coordinates": "24.78° N, 92.55° E",
            "latitude": 24.78,
            "longitude": 92.55,
            "localities": "Algapur, Mohanpur, Kalinagar, Barak Bank",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Hojai": [
        {
            "zone_name": "Northern Sector (Doboka & Jamunamukh Kopili Basin)",
            "coordinates": "26.12° N, 92.88° E",
            "latitude": 26.12,
            "longitude": 92.88,
            "localities": "Doboka, Jamunamukh, Kopili-Jamuna Confluence",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Hojai Town & Sankardev Nagar District HQ)",
            "coordinates": "26.00° N, 92.86° E",
            "latitude": 26.00,
            "longitude": 92.86,
            "localities": "Hojai City, Sankardev Nagar, DC Office, Lanka Belt",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Lumding Railway Corridor & Karbi Foothills)",
            "coordinates": "25.75° N, 93.17° E",
            "latitude": 25.75,
            "longitude": 93.17,
            "localities": "Lumding Town, Railway Junction, Karbi Foothills",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Jorhat": [
        {
            "zone_name": "Northern Sector (Teok & Nimati Ghat Brahmaputra Bank)",
            "coordinates": "26.85° N, 94.35° E",
            "latitude": 26.85,
            "longitude": 94.35,
            "localities": "Teok, Nimati Ghat, Brahmaputra Ferry Terminal, Riverine Chars",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Jorhat Urban & Cultural Core)",
            "coordinates": "26.75° N, 94.22° E",
            "latitude": 26.75,
            "longitude": 94.22,
            "localities": "Jorhat City, Cinnamara Tea Hub, DC Office, Agricultural University",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Titabar & Mariani Nagaland Foothills)",
            "coordinates": "26.58° N, 94.18° E",
            "latitude": 26.58,
            "longitude": 94.18,
            "localities": "Titabar, Mariani, Gibbon Sanctuary Belt, Nagaland Border",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Kamrup": [
        {
            "zone_name": "Northern Sector (Rangia & Kamalpur North Bank Corridor)",
            "coordinates": "26.45° N, 91.62° E",
            "latitude": 26.45,
            "longitude": 91.62,
            "localities": "Rangia Junction, Kamalpur, Hajo Historic Circuit, Puthimari",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Amingaon HQ & Palasbari Riverfront)",
            "coordinates": "26.18° N, 91.68° E",
            "latitude": 26.18,
            "longitude": 91.68,
            "localities": "Amingaon DC Office, Mirza, Palasbari, Sualkuchi Silk Belt",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Boko & Chaygaon Kulsi Meghalaya Basin)",
            "coordinates": "25.98° N, 91.22° E",
            "latitude": 25.98,
            "longitude": 91.22,
            "localities": "Boko, Chaygaon, Kulsi River Dolphin Habitat, Singra",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Kamrup Metropolitan": [
        {
            "zone_name": "Southern Sector (Dispur Capital & Basistha Ridge)",
            "coordinates": "26.14° N, 91.79° E",
            "latitude": 26.14,
            "longitude": 91.79,
            "localities": "Dispur Secretariat, Basistha, Khanapara, Meghalaya Ridge Foot",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Guwahati Urban Core & Bharalu Basin)",
            "coordinates": "26.18° N, 91.75° E",
            "latitude": 26.18,
            "longitude": 91.75,
            "localities": "Paltan Bazar, Panbazar, Bharalumukh, Zoo Road, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Northern Sector (Brahmaputra Waterfront & North Guwahati)",
            "coordinates": "26.21° N, 91.72° E",
            "latitude": 26.21,
            "longitude": 91.72,
            "localities": "Uzanbazar Riverfront, North Guwahati, IIT Guwahati Belt, Pandu Port",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Karbi Anglong": [
        {
            "zone_name": "Northern Sector (Howraghat & Phuloni Jamuna Valley)",
            "coordinates": "26.15° N, 93.05° E",
            "latitude": 26.15,
            "longitude": 93.05,
            "localities": "Howraghat, Phuloni, Jamuna River Agricultural Plain",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Diphu HQ & Karbi Central Mountain Core)",
            "coordinates": "26.03° N, 93.43° E",
            "latitude": 26.03,
            "longitude": 93.43,
            "localities": "Diphu Town, Manja, Karbi Hills Council HQ, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Eastern Sector (Bokajan & Khatkhati Dimapur Border)",
            "coordinates": "25.92° N, 93.78° E",
            "latitude": 25.92,
            "longitude": 93.78,
            "localities": "Bokajan, Khatkhati, Dhansiri Valley, Dimapur Border",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Karimganj": [
        {
            "zone_name": "Southern Sector (Patharkandi & Tripura Border Hills)",
            "coordinates": "24.60° N, 92.32° E",
            "latitude": 24.60,
            "longitude": 92.32,
            "localities": "Patharkandi, Lowairpoa, Churaibari Tripura Border",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Karimganj Town & Longai Valley)",
            "coordinates": "24.87° N, 92.35° E",
            "latitude": 24.87,
            "longitude": 92.35,
            "localities": "Karimganj Town, Nilambazar, Longai Riverbank, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Northern Sector (Badarpur & Kushiara Confluence)",
            "coordinates": "24.90° N, 92.55° E",
            "latitude": 24.90,
            "longitude": 92.55,
            "localities": "Badarpur, Bhanga, Kushiara River Confluence",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Kokrajhar": [
        {
            "zone_name": "Northern Sector (Kachugaon & Ultapani Bhutan Foothill Forest)",
            "coordinates": "26.65° N, 90.15° E",
            "latitude": 26.65,
            "longitude": 90.15,
            "localities": "Kachugaon, Ultapani Forest Reserve, Saralbhanga Watershed",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Kokrajhar Town & Bodoland Secretariat Core)",
            "coordinates": "26.40° N, 90.27° E",
            "latitude": 26.40,
            "longitude": 90.27,
            "localities": "Kokrajhar Town, Dotma, BTC Secretariat, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Western Sector (Gossaigaon & Sankosh Bengal Interstate Corridor)",
            "coordinates": "26.45° N, 89.98° E",
            "latitude": 26.45,
            "longitude": 89.98,
            "localities": "Gossaigaon, Bhavabil, Sankosh River Basin, Bengal Border",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Lakhimpur": [
        {
            "zone_name": "Northern Sector (Naoboicha & Ranganadi Dam Outfall Corridor)",
            "coordinates": "27.35° N, 94.05° E",
            "latitude": 27.35,
            "longitude": 94.05,
            "localities": "Naoboicha, Banderdewa Border, Ranganadi Dam Outfall, Dikrong",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (North Lakhimpur HQ & Commercial Belt)",
            "coordinates": "27.23° N, 94.10° E",
            "latitude": 27.23,
            "longitude": 94.10,
            "localities": "North Lakhimpur City, Lilabari Airport Belt, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Dhakuakhana & Subansiri Alluvial Floodplain)",
            "coordinates": "27.12° N, 94.45° E",
            "latitude": 27.12,
            "longitude": 94.45,
            "localities": "Dhakuakhana, Bihpuria, Narayanpur, Subansiri Basin",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Majuli": [
        {
            "zone_name": "Northern Sector (Jengraimukh & Subansiri Northern Confluence)",
            "coordinates": "27.05° N, 94.30° E",
            "latitude": 27.05,
            "longitude": 94.30,
            "localities": "Jengraimukh, Kherkatia Suti, Subansiri River Entry",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Garmur HQ & Kamalabari Cultural Core)",
            "coordinates": "26.95° N, 94.21° E",
            "latitude": 26.95,
            "longitude": 94.21,
            "localities": "Garmur HQ, Kamalabari, Auniati Satra, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Ahotguri & Brahmaputra South Floodplain)",
            "coordinates": "26.85° N, 94.10° E",
            "latitude": 26.85,
            "longitude": 94.10,
            "localities": "Ahotguri, Dakhinpat, Brahmaputra Southern Active Bank",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Morigaon": [
        {
            "zone_name": "Northern Sector (Bhuragaon & Laharighat Brahmaputra Active Bank)",
            "coordinates": "26.35° N, 92.42° E",
            "latitude": 26.35,
            "longitude": 92.42,
            "localities": "Bhuragaon, Laharighat, Brahmaputra High Flood Bank",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Morigaon Town & Mikirbheta Administrative Core)",
            "coordinates": "26.25° N, 92.34° E",
            "latitude": 26.25,
            "longitude": 92.34,
            "localities": "Morigaon Town, Mikirbheta, Jagiroad Industrial Belt, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Western Sector (Mayong & Pobitora Wildlife Killing Corridor)",
            "coordinates": "26.20° N, 92.05° E",
            "latitude": 26.20,
            "longitude": 92.05,
            "localities": "Mayong, Pobitora Wildlife Sanctuary, Killing River Basin",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Nagaon": [
        {
            "zone_name": "Northern Sector (Kaliabor & Silghat Brahmaputra Riverfront)",
            "coordinates": "26.55° N, 92.95° E",
            "latitude": 26.55,
            "longitude": 92.95,
            "localities": "Kaliabor, Silghat Port, Samaguri Lake, Kolia Bhomora East",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Nagaon City & Kolong River Administrative Core)",
            "coordinates": "26.35° N, 92.68° E",
            "latitude": 26.35,
            "longitude": 92.68,
            "localities": "Nagaon City, Haiborgaon, Kolong Riverbanks, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Raha & Kampur Kopili Flash Flood Basin)",
            "coordinates": "26.15° N, 92.70° E",
            "latitude": 26.15,
            "longitude": 92.70,
            "localities": "Raha, Kampur, Kopili River Basin, Dhing Corridor",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Nalbari": [
        {
            "zone_name": "Northern Sector (Bhutan Foothills & Pagladiya Entry - Ghograpar / Tihu)",
            "coordinates": "26.55° N, 91.48° E",
            "latitude": 26.55,
            "longitude": 91.48,
            "localities": "Ghograpar, Tihu, Dhamdhama, Subankhata Baksa Border",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Nalbari Town & Administrative Core)",
            "coordinates": "26.44° N, 91.44° E",
            "latitude": 26.44,
            "longitude": 91.44,
            "localities": "Nalbari City, DC Office, Barbhag Corridor, Hajo Road",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Barkhetri & Brahmaputra Alluvial Basin)",
            "coordinates": "26.30° N, 91.35° E",
            "latitude": 26.30,
            "longitude": 91.35,
            "localities": "Barkhetri, Mukalmua, Brahmaputra Riverine Chars",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Sivasagar": [
        {
            "zone_name": "Northern Sector (Demow & Disangmukh Brahmaputra Floodplain)",
            "coordinates": "27.15° N, 94.75° E",
            "latitude": 27.15,
            "longitude": 94.75,
            "localities": "Demow, Disangmukh, Disang-Brahmaputra Confluence",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Sivasagar City & Historical Joysagar Core)",
            "coordinates": "26.98° N, 94.63° E",
            "latitude": 26.98,
            "longitude": 94.63,
            "localities": "Sivasagar City, Joysagar, Dikhow Riverfront, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Nazira & Amguri Nagaland Border Belt)",
            "coordinates": "26.85° N, 94.70° E",
            "latitude": 26.85,
            "longitude": 94.70,
            "localities": "Nazira, Amguri, Geleky Oil Fields, Nagaland Foothills",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Sonitpur": [
        {
            "zone_name": "Northern Sector (Chariduar & Bhalukpong Jia Bhareli Gorge)",
            "coordinates": "26.85° N, 92.78° E",
            "latitude": 26.85,
            "longitude": 92.78,
            "localities": "Chariduar, Bhalukpong Border, Nameri National Park, Jia Bhareli Entry",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Tezpur City & Historic Kolia Bhomora Core)",
            "coordinates": "26.63° N, 92.79° E",
            "latitude": 26.63,
            "longitude": 92.79,
            "localities": "Tezpur City, Mission Chariali, DC Office, Brahmaputra Riverfront",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Western Sector (Dhekiajuli & Thelamara Agricultural Plains)",
            "coordinates": "26.70° N, 92.50° E",
            "latitude": 26.70,
            "longitude": 92.50,
            "localities": "Dhekiajuli, Thelamara, Gabharu River Basin",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "South Salmara-Mankachar": [
        {
            "zone_name": "Northern Sector (South Salmara & Brahmaputra Active Chars)",
            "coordinates": "25.88° N, 89.85° E",
            "latitude": 25.88,
            "longitude": 89.85,
            "localities": "South Salmara, Fekamari, Brahmaputra Island Chars",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Hatsingimari District HQ Core)",
            "coordinates": "25.75° N, 89.85° E",
            "latitude": 25.75,
            "longitude": 89.85,
            "localities": "Hatsingimari Town, Sukchar, DC Office Complex",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Mankachar & Meghalaya-Bangladesh Border Belt)",
            "coordinates": "25.53° N, 89.86° E",
            "latitude": 25.53,
            "longitude": 89.86,
            "localities": "Mankachar, Kalaichar Border Trade Post, Garo Foothills",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Tamulpur": [
        {
            "zone_name": "Northern Sector (Nagrijuli & Kumarikata Bhutan Border Foothills)",
            "coordinates": "26.75° N, 91.60° E",
            "latitude": 26.75,
            "longitude": 91.60,
            "localities": "Nagrijuli, Kumarikata, Bhutan International Boundary, Borolia Upper Reach",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Tamulpur Town & Borolia River Corridor)",
            "coordinates": "26.63° N, 91.57° E",
            "latitude": 26.63,
            "longitude": 91.57,
            "localities": "Tamulpur Town, Borolia Basin, DC Office, Goybari",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Goreswar & Rangia Border Alluvial Plains)",
            "coordinates": "26.50° N, 91.68° E",
            "latitude": 26.50,
            "longitude": 91.68,
            "localities": "Goreswar, Rangia Border Corridor, Puthimari Basin",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Tinsukia": [
        {
            "zone_name": "Northern Sector (Sadiya & Chapakhowa Kundil River Basin)",
            "coordinates": "27.82° N, 95.65° E",
            "latitude": 27.82,
            "longitude": 95.65,
            "localities": "Sadiya, Chapakhowa, Kundil River Trans-Brahmaputra",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Tinsukia City & Doomdooma Commercial Hub)",
            "coordinates": "27.50° N, 95.36° E",
            "latitude": 27.50,
            "longitude": 95.36,
            "localities": "Tinsukia City, Doomdooma, Digboi Refinery Town, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Margherita & Ledo Dehing Patkai Rainforest)",
            "coordinates": "27.28° N, 95.68° E",
            "latitude": 27.28,
            "longitude": 95.68,
            "localities": "Margherita, Ledo, Dehing Patkai Hills, Burhi Dihing Corridor",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "Udalguri": [
        {
            "zone_name": "Northern Sector (Bhairabkunda Tri-Junction & Bornadi Sanctuary)",
            "coordinates": "26.88° N, 92.15° E",
            "latitude": 26.88,
            "longitude": 92.15,
            "localities": "Bhairabkunda (Bhutan-Arunachal-Assam Tri-junction), Bornadi Sanctuary",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Udalguri Town & Dhansiri North Basin)",
            "coordinates": "26.75° N, 92.10° E",
            "latitude": 26.75,
            "longitude": 92.10,
            "localities": "Udalguri Town, Harisinga, Dhansiri North Basin, DC Office",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Southern Sector (Rowta & Mazbat BTR Agricultural Plains)",
            "coordinates": "26.60° N, 92.20° E",
            "latitude": 26.60,
            "longitude": 92.20,
            "localities": "Rowta, Mazbat, Kalaigaon, Orang National Park Border",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ],
    "West Karbi Anglong": [
        {
            "zone_name": "Northern Sector (Donkamukam & Kopili River Outfall Valley)",
            "coordinates": "25.98° N, 92.68° E",
            "latitude": 25.98,
            "longitude": 92.68,
            "localities": "Donkamukam, Kopili River Agricultural Valley, Kheroni",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Central Sector (Hamren District HQ & Karbi Plateau Ridges)",
            "coordinates": "25.85° N, 92.55° E",
            "latitude": 25.85,
            "longitude": 92.55,
            "localities": "Hamren Town, DC Office, Karbi Plateau Core, Rongkhang",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        },
        {
            "zone_name": "Western Sector (Baithalangso & Khanduli Meghalaya Border)",
            "coordinates": "25.72° N, 92.40° E",
            "latitude": 25.72,
            "longitude": 92.40,
            "localities": "Baithalangso, Khanduli, Umkhen River Border, Ri Bhoi Border",
            "alert_level": "Green Alert (No Warning)",
            "alert_color": "Green",
            "hazard_phenomenon": "Normal Weather / No Severe Phenomenon",
            "expected_winds": "💨 Light to Gentle Breeze (10 - 20 km/h)",
            "action_suggested": "Normal daily operations permitted.",
            "convective_status": "Atmospheric stability prevailing."
        }
    ]
}


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
        elif lat > 26.2 and lon < 92.5:  # Lower Assam North Bank
            default_states = ["Assam", "West Bengal"]
            default_districts = ["Baksa", "Alipurduar"]
            basin = "Lower Brahmaputra North Bank Basin"
            subdiv = "Lower Assam North Bank"
        elif lon < 91.5:  # Lower Assam South Bank
            default_states = ["Meghalaya", "West Bengal"]
            default_districts = ["West Garo Hills", "Alipurduar"]
            basin = "Lower Brahmaputra South Bank Basin"
            subdiv = "Lower Assam"
        else:  # Central Assam
            default_states = ["Meghalaya", "Nagaland"]
            default_districts = ["Ri Bhoi", "Wokha"]
            basin = "Central Brahmaputra Basin"
            subdiv = "Central Assam"

    # Extract authentic verified revenue circle sectors
    sectors = ASSAM_DISTRICTS_SECTORS_REGISTRY.get(district_name, [])

    return {
        "lat": lat,
        "lon": lon,
        "district_id": 300,
        "river_basin": basin,
        "subdivision": subdiv,
        "bbox": {"min_lat": round(lat - 0.35, 2), "max_lat": round(lat + 0.35, 2), "min_lon": round(lon - 0.35, 2), "max_lon": round(lon + 0.35, 2)},
        "default_secondary_states": default_states,
        "default_secondary_districts": default_districts,
        "sectors": sectors
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
