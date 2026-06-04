
// AI HUB LOGIC - BULLETPROOF REWRITE
(function() {
    const BUILD_STEPS = [
        { id: 'frame',      name: 'Kadro (Frame)',                    freetext: true },
        { id: 'headset',    name: 'Furç Takımı (Headset)' },
        { id: 'fork',       name: 'Maşa (Fork)' },
        { id: 'shock',      name: 'Arka Şok (Rear Shock)' },
        { id: 'bb',         name: 'Orta Göbek (Bottom Bracket)' },
        { id: 'crank',      name: 'Aynakol (Crankset)' },
        { id: 'chainguide', name: 'Zincir Gergisi (Chainguide)' },
        { id: 'derailleur', name: 'Arka Aktarıcı (Rear Derailleur)' },
        { id: 'shifter',    name: 'Vites Kolu (Shifter)' },
        { id: 'cassette',   name: 'Kaset (Cassette)' },
        { id: 'chain',      name: 'Zincir (Chain)' },
        { id: 'brakes',     name: 'Fren Seti (Brakes)' },
        { id: 'rotors',     name: 'Fren Diskleri (Rotors)' },
        { id: 'wheels',     name: 'Jant Seti (Wheelset)' },
        { id: 'tires',      name: 'Lastikler (Tires)' },
        { id: 'handlebar',  name: 'Gidon (Handlebar)' },
        { id: 'stem',       name: 'Gidon Boğazı (Stem)' },
        { id: 'grips',      name: 'Elcik (Grips)' },
        { id: 'seatpost',   name: 'Sele Borusu / Dropper (Seatpost)' },
        { id: 'saddle',     name: 'Sele (Saddle)' },
        { id: 'pedals',     name: 'Pedallar (Pedals)' },
        { id: 'extras',     name: 'Ekstralar (Örn: Çamurluk vs)',    freetext: true }
    ];

    // =========================================================
    // KAPSAMLI PARÇA VERİTABANI — Marka → Model
    // =========================================================
    const PARTS_DB = {
        frame: {
            'Santa Cruz': ['V10', 'Megatower', 'Nomad', 'Bronson', 'Hightower', 'Tallboy', 'Bullit (E-Bike)', 'Heckler (E-Bike)', 'Chameleon', 'Blur', 'Highball', 'Stigmata'],
            'Trek': ['Session', 'Slash', 'Remedy', 'Fuel EX', 'Fuel EXe', 'Top Fuel', 'Rail (E-Bike)', 'Powerfly (E-Bike)', 'Marlin', 'Roscoe', 'Procaliber', 'Supercaliber', 'Ticket'],
            'Specialized': ['Demo', 'Enduro', 'Stumpjumper EVO', 'Stumpjumper', 'Epic', 'Epic EVO', 'Chisel', 'Fuse', 'Status', 'Levo (E-Bike)', 'Levo SL (E-Bike)', 'Kenevo (E-Bike)', 'Kenevo SL (E-Bike)'],
            'Canyon': ['Sender', 'Torque', 'Strive', 'Spectral', 'Neuron', 'Lux', 'Exceed', 'Grand Canyon', 'Stoic', 'Torque:ON', 'Spectral:ON', 'Neuron:ON', 'Grand Canyon:ON'],
            'YT Industries': ['Tues', 'Capra', 'Jeffsy', 'Izzo', 'Szepter', 'Dirt Love', 'Decoy (E-Bike)'],
            'Commencal': ['Supreme DH', 'Furious', 'Clash', 'Meta AM', 'Meta SX', 'Meta TR', 'Meta HT AM', 'Absolut', 'Meta Power TR', 'Meta Power SX'],
            'Nukeproof': ['Dissent', 'Mega', 'Giga', 'Reactor', 'Scout', 'Megawatt (E-Bike)'],
            'Transition': ['TR11', 'Spire', 'Patrol', 'Sentinel', 'Scout', 'Smuggler', 'Spur', 'PBJ', 'Relay (E-Bike)', 'Repeater (E-Bike)'],
            'Evil': ['Wreckoning', 'Insurgent', 'Offering', 'Following', 'Chamois Hagar', 'Faction', 'Epocalypse (E-Bike)'],
            'Yeti': ['SB165', 'SB160', 'SB150', 'SB140', 'SB135', 'SB130', 'SB120', 'SB115', 'ARC', '160E (E-Bike)'],
            'Giant': ['Glory', 'Reign', 'Trance X', 'Trance', 'Anthem', 'XTC', 'Fathom', 'Talon', 'Stance', 'Reign E+', 'Trance X E+', 'Stance E+', 'Talon E+'],
            'Scott': ['Gambler', 'Ransom', 'Genius', 'Spark', 'Scale', 'Aspect', 'Voltage', 'Ransom eRIDE', 'Genius eRIDE', 'Strike eRIDE', 'Patron eRIDE', 'Lumen eRIDE'],
            'Propain': ['Rage', 'Spindrift', 'Tyee', 'Hugene', 'Trickshot', 'Ekano (E-Bike)'],
            'Pivot': ['Phoenix', 'Firebird', 'Mach 6', 'Switchblade', 'Trail 429', 'Mach 4 SL', 'LES SL', 'Shuttle LT', 'Shuttle AM', 'Shuttle SL'],
            'Orbea': ['Rallon', 'Occam LT', 'Occam SL', 'Oiz', 'Alma', 'Laufey', 'Onna', 'Wild', 'Rise', 'Urrun', 'Keram'],
            'Ibis': ['Ripmo', 'Ripmo AF', 'Ripley', 'Ripley AF', 'Mojo HD5', 'Mojo 4', 'Exie', 'Oso (E-Bike)'],
            'Norco': ['Aurum HSP', 'Shore', 'Range', 'Sight', 'Optic', 'Fluid FS', 'Fluid HT', 'Revolver', 'Torrent', 'Rampage', 'Range VLT', 'Sight VLT', 'Fluid VLT'],
            'Devinci': ['Wilson', 'Spartan', 'Troy', 'Marshall', 'Django', 'Kobain', 'AC (E-Bike)', 'DC (E-Bike)', 'E-Troy', 'E-Spartan'],
            'Rocky Mountain': ['Maiden', 'Slayer', 'Altitude', 'Instinct', 'Element', 'Growler', 'Soul', 'Vertex', 'Altitude Powerplay', 'Instinct Powerplay', 'Growler Powerplay'],
            'Kona': ['Operator', 'Process X', 'Process 153', 'Process 134', 'Hei Hei', 'Honzo', 'Honzo ESD', 'Big Honzo', 'Kahuna', 'Remote (E-Bike)', 'Remote 160'],
            'GT': ['Fury', 'Force', 'Sensor', 'Zaskar', 'Avalanche', 'Aggressor', 'La Bomba', 'Force AMP', 'Pantera AMP'],
            'Merida': ['One-Sixty', 'One-Forty', 'One-Twenty', 'Ninety-Six', 'Big.Nine', 'Big.Trail', 'Matts', 'eOne-Sixty', 'eOne-Forty', 'eBig.Nine'],
            'Cube': ['Two15', 'Stereo ONE77', 'Stereo ONE55', 'Stereo ONE44', 'Stereo ONE22', 'Reaction', 'Attention', 'Analog', 'Aim', 'Stereo Hybrid 160', 'Stereo Hybrid 140', 'Stereo Hybrid 120', 'Reaction Hybrid'],
            'Marin': ['Alpine Trail', 'Rift Zone', 'San Quentin', 'Bobcat Trail', 'Bolinas Ridge', 'El Roy', 'Pine Mountain', 'Alpine Trail E', 'Rift Zone E'],
            'Mondraker': ['Summum', 'Superfoxy', 'Foxy', 'Raze', 'Podium', 'Chrono', 'Level (E-Bike)', 'Crafty (E-Bike)', 'Chaser (E-Bike)', 'Dusk (E-Bike)', 'Prime (E-Bike)'],
            'Ghost': ['Riot EN', 'Riot AM', 'Riot Trail', 'Lector', 'Nirvana', 'Kato', 'E-Riot EN', 'E-Riot AM', 'E-Riot Trail', 'E-Teru'],
            'Polygon': ['Collosus DH', 'Collosus N9', 'Siskiu T', 'Siskiu D', 'Xtrada', 'Premier', 'Cascade', 'Mt Bromo (E-Bike)', 'Siskiu TE (E-Bike)']
        },
        headset: {
            'Chris King': ['InSet 1 (EC49/40)', 'InSet 2 (EC49/40)', 'InSet 3', 'InSet 7 (EC49/40)', 'InSet 8 (ZS49/EC49)', 'NoThreadSet (ZS44)', 'NoThreadSet (EC49)', 'ThreadFit 40 (ZS56)', 'GripNut', 'Dropset 1', 'Dropset 2', 'Dropset 3', 'Dropset 4', 'Dropset 5'],
            'Cane Creek': ['40 Series (ZS44/ZS56)', '40 Series (IS41/IS52)', '40 Series (EC34/EC44)', '110 Series (ZS44/ZS56)', '110 Series (IS41/IS52)', 'Hellbender 70 (ZS44/ZS56)', 'Hellbender 70 (IS41/IS52)', 'ViscoSet', 'AER', 'SlamSet'],
            'FSA': ['Orbit C-40', 'Orbit 1.5 ZS', 'Orbit Z', 'No.10', 'No.57E', 'No.42/ACB', 'No.55R', 'No.69', 'DX Pro', 'The Pig DH Pro', 'Orbit MX'],
            'Ritchey': ['WCS Logic Drop In', 'WCS Press Fit', 'WCS Zero', 'Comp Logic', 'Comp Zero', 'Classic'],
            'Hope': ['Pick n Mix (Custom)', 'Traditional', 'Integral', 'Internal (Zero Stack)', 'Integrated (IS)'],
            'Nukeproof': ['Horizon 44IETS', 'Horizon 44-56IITS', 'Neutron', 'Warhead'],
            'Wolf Tooth': ['Premium IS', 'Premium ZS', 'Premium EC', 'Performance IS', 'Performance ZS', 'Performance EC', 'GeoShift Angle Headset'],
            'Acros': ['AZX-203', 'AZX-212', 'AZX-226', 'AZX-252', 'AZX-258', 'Blocklock', 'ZS44/ZS56', 'IS41/IS52'],
            'Token': ['Omega A83', 'Omega C83', 'Ninja', 'Kudos'],
            'Brand-X': ['Sealed Integrated', 'Sealed ZS44/ZS56', 'Sealed EC34/EC44'],
            'First': ['DS-1', 'Z1', 'R1']
        },
        fork: {
            'Fox': ['32 Float Step-Cast Factory', '32 Float Step-Cast Performance', '32 Float Rhythm', '34 Float Factory', '34 Float Performance Elite', '34 Float Performance', '34 Float Rhythm', '34 Step-Cast Factory', '34 Step-Cast Performance', '36 Float Factory', '36 Float Performance Elite', '36 Float Performance', '36 Float Rhythm', '38 Float Factory', '38 Float Performance Elite', '38 Float Performance', '40 Float Factory', '40 Float Performance'],
            'RockShox': ['Judy Silver TK', 'Judy Gold RL', 'Recon Silver RL', 'Recon Gold RL', '35 Silver TK', '35 Gold RL', 'Bluto', 'Reba RL', 'SID SL Select', 'SID SL Ultimate', 'SID Select', 'SID Select+', 'SID Ultimate', 'Revelation RC', 'Pike Select', 'Pike Select+', 'Pike Ultimate', 'Lyrik Select', 'Lyrik Select+', 'Lyrik Ultimate', 'Zeb Select', 'Zeb Select+', 'Zeb Ultimate', 'Domain RC', 'Domain Select', 'BoXXer Select', 'BoXXer Ultimate'],
            'Manitou': ['Markhor', 'Machete', 'Machete JUNIT', 'Circus Sport', 'Circus Expert', 'Circus Pro', 'Mattoc Comp', 'Mattoc Expert', 'Mattoc Pro', 'Mezzer Expert', 'Mezzer Pro', 'Dorado Comp', 'Dorado Expert', 'Dorado Pro', 'Mastodon Comp', 'Mastodon Pro'],
            'Marzocchi': ['Bomber Z2', 'Bomber Z1 Air', 'Bomber Z1 Coil', 'Bomber 58', 'Bomber DJ'],
            'Öhlins': ['RXF34 m.2', 'RXF36 m.2 Air', 'RXF36 m.2 Coil', 'RXF38 m.2', 'DH38 m.1'],
            'DVO': ['Sapphire D1', 'Diamond D1', 'Diamond D2', 'Onyx SC D1', 'Onyx DC D1', 'Beryl'],
            'SR Suntour': ['XCT', 'XCM', 'XCR 32', 'XCR 34', 'Raidon 32', 'Raidon 34', 'Epixon', 'Axon 32', 'Axon 34', 'Aion 35', 'Auron 35', 'Durolux 36', 'Durolux 38', 'Rux 38'],
            'Formula': ['33', '35', 'Selva R', 'Selva S', 'Selva C', 'Nero C', 'Nero R'],
            'Cane Creek': ['Helm MKII Air', 'Helm MKII Coil'],
            'EXT': ['Era V2', 'Era V2 LT', 'Ferro'],
            'Trust Performance': ['Message', 'Shout'],
            'RST': ['Gila', 'Blaze', 'Omega', 'Aerial', 'First', 'Rogue', 'Stitch', 'Killah'],
            'Magura': ['TS6', 'TS8', 'Boltron (E-Bike)'],
            'Cannondale': ['Lefty Ocho', 'Lefty Ocho Carbon', 'Lefty Supermax', 'Lefty Oliver']
        },
        shock: {
            'Fox': ['Float DPS Performance', 'Float DPS Performance Elite', 'Float DPS Factory', 'Float SL', 'Float X Performance', 'Float X Performance Elite', 'Float X Factory', 'Float X2 Performance', 'Float X2 Factory', 'DHX Performance', 'DHX Factory', 'DHX2 Performance Elite', 'DHX2 Factory', 'Float DPX2'],
            'RockShox': ['Monarch R', 'Monarch RT3', 'Monarch Plus RC3', 'Deluxe Select', 'Deluxe Select+', 'Deluxe Ultimate', 'Super Deluxe Select', 'Super Deluxe Select+', 'Super Deluxe Ultimate', 'Super Deluxe Coil Select', 'Super Deluxe Coil Select+', 'Super Deluxe Coil Ultimate', 'Vivid Air', 'Vivid Coil', 'Kage RC'],
            'Öhlins': ['TTX1 Air', 'TTX2 Air', 'TTX22M.2 Coil', 'TTX Flow'],
            'Cane Creek': ['DB IL Air', 'DB IL Coil', 'Kitsuma Air', 'Kitsuma Coil'],
            'Marzocchi': ['Bomber Air', 'Bomber CR'],
            'DVO': ['Topaz T3 Air', 'Topaz 2', 'Topaz 3', 'Jade Coil', 'Jade X Coil'],
            'EXT': ['Storia LOK V3', 'Arma V3', 'Aria'],
            'Push': ['ElevenSix', 'SV8'],
            'Manitou': ['Mara Inline', 'Mara Pro'],
            'Formula': ['Mod'],
            'SR Suntour': ['Raidon R', 'Epixon R', 'Triair 3CR', 'Triair2 3CR', 'Voro'],
            'X-Fusion': ['O2 Pro RL', 'O2 Pro RCX', 'Vector Air HLR', 'Vector Coil HLR', 'H3C Coil'],
            'Fast Suspension': ['Fenix Evo', 'Holy Grail']
        },
        bb: {
            'Shimano': ['BB-UN101 (Square Taper)', 'BB-UN300 (Square Taper)', 'BB-MT500 (Hollowtech II)', 'BB-MT501', 'SM-BB52', 'BB-MT800', 'BB-MT801', 'SM-BB93', 'BB-MT500-PA (Press-Fit)', 'BB-MT800-PA', 'SM-BB71-41A', 'SM-BB94-41A'],
            'SRAM': ['Power Spline', 'Howitzer XR', 'Howitzer Team', 'GXP XR', 'GXP Team', 'PressFit GXP', 'DUB BSA 68/73', 'DUB BSA 83', 'DUB PressFit 89/92', 'DUB PressFit 104.5/107', 'DUB BB30', 'DUB PF30'],
            'Race Face': ['BSA 24mm', 'BSA 30mm', 'Cinch BSA 30', 'PF30 24mm', 'PF30 30mm', 'BB92 24mm', 'BB92 30mm'],
            'Hope': ['Stainless Steel BSA 24mm', 'Stainless Steel BSA 30mm', 'PressFit 41 24mm', 'PressFit 41 30mm', 'PressFit 46 24mm', 'PressFit 46 30mm'],
            'Chris King': ['ThreadFit 24', 'ThreadFit 30', 'PressFit 24', 'PressFit 30', 'ThreadFit T47'],
            'Cane Creek': ['Hellbender 70 BSA', 'Hellbender 70 PF41', 'Hellbender 70 PF30', 'Hellbender 70 BB30', 'Hellbender 70 T47', 'Hellbender Neo (Ceramic)'],
            'Wheels Manufacturing': ['BSA 24', 'BSA 30', 'BB86/92 to 24', 'BB86/92 to 30', 'PF30 Outboard', 'BB30 Outboard', 'T47 Outboard'],
            'Token': ['Ninja Lite (PF)', 'Ninja (Threaded PF)', 'Ninja Token ThreadFit', 'VGM BB'],
            'FSA': ['MegaExo', 'MegaEvo', 'BB30', 'PF30', 'BB392EVO', 'Platinum Pro (ISIS)'],
            'Praxis Works': ['M30 BSA', 'M30 BB86/92', 'M30 BB30/PF30', 'M30 T47', 'Shimano BB30/PF30 Conv']
        },
        crank: {
            'Shimano': ['Tourney FC-TY301', 'Tourney FC-TY501', 'Altus FC-M311', 'Altus FC-MT101', 'Acera FC-M361', 'Acera FC-MT210', 'Alivio FC-M4050', 'Alivio FC-M3100', 'Deore FC-M4100-2', 'Deore FC-M5100-1', 'Deore FC-M5100-2', 'Deore FC-M6100-1', 'Deore FC-M6120-1', 'Deore FC-M6130-1', 'SLX FC-M7100-1', 'SLX FC-M7120-1', 'SLX FC-M7130-1', 'XT FC-M8100-1', 'XT FC-M8120-1', 'XT FC-M8130-1', 'XTR FC-M9100-1', 'XTR FC-M9120-1', 'ZEE FC-M640', 'Saint FC-M820', 'Saint FC-M825', 'FC-MT511', 'FC-MT611'],
            'SRAM': ['SX Eagle', 'NX Eagle', 'GX Eagle', 'GX Eagle Carbon', 'X1 Carbon', 'X01 Eagle', 'X01 Eagle DUB', 'XX1 Eagle', 'XX1 Eagle DUB', 'X0 Eagle Transmission', 'XX Eagle Transmission', 'XX SL Eagle Transmission', 'Descendant 6K', 'Descendant 7K', 'Descendant Carbon', 'Stylo 6K', 'Stylo 7K', 'Stylo Carbon'],
            'Race Face': ['Ride', 'Chester', 'Aeffect', 'Aeffect R', 'Turbine', 'Turbine R', 'Atlas', 'Next R', 'Next SL', 'Era'],
            'Hope': ['Evo', 'Evo e-Bike', 'RX'],
            'e*thirteen': ['Base', 'Helix Core', 'Helix Race', 'LG1 Plus', 'LG1 Race Carbon', 'TRS Plus', 'TRS Race Carbon', 'XCX Race Carbon'],
            'Truvativ': ['Hussefelt', 'Holzfeller', 'Descendant (Alloy/Carbon)', 'Stylo (Alloy/Carbon)'],
            'FSA': ['Alpha Drive', 'Gamma Pro', 'Comet', 'V-Drive', 'Afterburner', 'Gradient', 'K-Force', 'KFX'],
            'Cane Creek': ['eeWings Mountain Titanium', 'eeWings Raven'],
            'Rotor': ['Kapic', 'Kapic Carbon', 'RHawk', 'Raptor'],
            'Praxis Works': ['Cadet M30', 'Girder Carbon', 'Lyft Carbon'],
            'Miranda': ['Delta (E-Bike)', 'Kappa (E-Bike)'],
            'Suntour': ['XCC', 'XCE', 'XCM', 'Zeron'],
            'Prowheel': ['Charm', 'Zephyr', 'Claw', 'MPX']
        },
        chainguide: {
            'MRP': ['1x CS', '1x Alloy', '1x Carbon', 'AMg CS', 'AMg Alloy', 'AMg Carbon', 'SXg Alloy', 'SXg Carbon', 'G4 Alloy', 'G4 Carbon', 'XCG V2'],
            'e*thirteen': ['Base Guide', 'TRS Plus', 'TRS Race', 'LG1 Plus', 'LG1 Race', 'Vario Top Guide', 'XCX Plus', 'XCX Race'],
            'OneUp Components': ['Chainguide - ISCG05', 'Bash Guide - ISCG05', 'Chain Guide - High Direct Mount', 'Chain Guide - Low Direct Mount'],
            'Wolf Tooth': ['GnarWolf ISCG05', 'GnarWolf High Direct Mount', 'GnarWolf Seat Tube', 'LoneWolf Aero'],
            'Funnn': ['Zippa Lite', 'Zippa DH', 'Zippa Bash'],
            'Hope': ['Slick Guide', 'Dropper Guide'],
            'Mozartt': ['HXR', 'Presto', 'Presto Steel', 'Meno Carbon', 'Piano'],
            'Reverse Components': ['X11-Evo', 'X1-B', 'Colab'],
            'Shimano': ['SM-CD50', 'SM-CD800', 'STEPS E8000 Guide'],
            'Sixpack': ['Kamikaze', 'Vertic'],
            'AbsoluteBlack': ['Oval Guide ISCG05', 'Oval Guide HDM']
        },
        derailleur: {
            'Shimano': ['Tourney TY200', 'Tourney TY300', 'Tourney TX800', 'Altus M310', 'Altus M370', 'Altus M2000', 'Acera M360', 'Acera M3000', 'Acera M3020', 'Alivio M4000', 'Alivio M3100', 'Deore M592', 'Deore M6000 (10s GS/SGS)', 'Deore M5120 (10/11s)', 'Deore M5100 (11s)', 'Deore M6100 (12s)', 'SLX M670', 'SLX M7000 (11s)', 'SLX M7100 (12s)', 'SLX M7120 (12s)', 'XT M786', 'XT M8000 (11s GS/SGS)', 'XT M8100 (12s)', 'XT M8120 (12s)', 'XTR M986', 'XTR M9000 (11s)', 'XTR M9100 (12s GS/SGS)', 'XTR M9120 (12s)', 'Saint M820', 'ZEE M640 (SS/Freeride)', 'CUES U4000 (9s)', 'CUES U6000 (10/11s)', 'CUES U8000 (11s)'],
            'SRAM': ['X3 (7/8s/9s)', 'X4 (8/9s)', 'X5 (9/10s)', 'X7 (9/10s)', 'X9 (9/10s)', 'X0 (9/10s)', 'NX (11s)', 'GX (10/11s)', 'X1 (11s)', 'X01 (11s)', 'XX1 (11s)', 'SX Eagle (12s)', 'NX Eagle (12s)', 'GX Eagle (12s)', 'GX Eagle AXS (12s)', 'X01 Eagle (12s)', 'X01 Eagle AXS (12s)', 'XX1 Eagle (12s)', 'XX1 Eagle AXS (12s)', 'GX Eagle Transmission', 'X0 Eagle Transmission', 'XX Eagle Transmission', 'XX SL Eagle Transmission'],
            'microSHIFT': ['Mezzo (8/9s)', 'Marvo LT (9s)', 'XLE (10/11s)', 'Advent (9s)', 'Advent X (10s)', 'Acolyte (8s)', 'Sword (10s)'],
            'Box Components': ['Box Four (8s)', 'Box Three (9s)', 'Box Two (11s)', 'Box One (11s)'],
            'TRP': ['TR12 (12s)', 'DH7 (7s)', 'Evo7 (7s)', 'Evo12 (12s)'],
            'SunRace': ['M40 (7/8s)', 'M50 (8/9s)', 'M90 (9s)', 'MS (10s)', 'MX (10/11s)', 'MZ (12s)']
        },
        shifter: {
            'Shimano': ['Tourney RS35 (Revoshift)', 'Tourney TX50', 'Tourney EF41', 'Altus M310', 'Altus M315', 'Altus M2000', 'Acera M360', 'Acera M3000', 'Alivio M4000', 'Alivio M3100', 'Deore M590', 'Deore M6000', 'Deore M5100', 'Deore M6100', 'SLX M670', 'SLX M7000', 'SLX M7100', 'XT M780', 'XT M8000', 'XT M8100', 'XTR M980', 'XTR M9000', 'XTR M9100', 'Saint M820', 'ZEE M640', 'CUES U4000', 'CUES U6000', 'CUES U8000'],
            'SRAM': ['X3 Trigger', 'X4 Trigger', 'X5 Trigger', 'X7 Trigger', 'X9 Trigger', 'X0 Trigger', 'NX Trigger', 'GX Trigger', 'X1 Trigger', 'X01 Trigger', 'XX1 Trigger', 'SX Eagle Trigger', 'NX Eagle Trigger', 'GX Eagle Trigger', 'GX Eagle AXS Controller', 'X01 Eagle Trigger', 'X01 Eagle AXS Controller', 'XX1 Eagle Trigger', 'XX1 Eagle AXS Controller', 'Eagle AXS Pod Controller', 'Eagle AXS Pod Ultimate', 'Grip Shift NX/GX/X01/XX1'],
            'microSHIFT': ['Mezzo Trigger', 'XLE Trigger', 'Advent Trigger', 'Advent X Trigger', 'Advent X Pro Trigger', 'Acolyte Trigger', 'Thumb Shifters'],
            'Box Components': ['Box Four Shifter', 'Box Three Shifter', 'Box Two Shifter', 'Box One Shifter'],
            'TRP': ['TR12 Shifter', 'DH7 Shifter', 'Evo7 Shifter', 'Evo12 Shifter'],
            'SunRace': ['M40 Trigger', 'M50 Trigger', 'M90 Trigger', 'DLM (Trigger)']
        },
        cassette: {
            'Shimano': ['Tourney TZ500 (6/7s)', 'Tourney HG200 (7/8/9s)', 'Altus HG31 (8s)', 'Acera HG400 (9s)', 'Alivio HG400 (9s)', 'Deore HG50 (10s)', 'Deore HG500 (10s)', 'Deore M4100 (10s)', 'Deore M5100 (11s)', 'Deore M6100 (12s)', 'SLX HG81 (10s)', 'SLX M7000 (11s)', 'SLX M7100 (12s)', 'XT M771 (10s)', 'XT M8000 (11s)', 'XT M8100 (12s)', 'XTR M980 (10s)', 'XTR M9000 (11s)', 'XTR M9100 (12s)', 'Linkglide LG300', 'Linkglide LG400', 'Linkglide LG600', 'Linkglide LG700'],
            'SRAM': ['PG-730 (7s)', 'PG-820 (8s)', 'PG-850 (8s)', 'PG-920 (9s)', 'PG-950 (9s)', 'PG-970 (9s)', 'PG-1030 (10s)', 'PG-1050 (10s)', 'PG-1070 (10s)', 'PG-1130 (11s)', 'XG-1150 (11s)', 'XG-1175 (11s)', 'XG-1195 (11s)', 'XG-1199 (11s)', 'PG-1210 (SX 12s)', 'PG-1230 (NX 12s)', 'XG-1275 (GX 12s)', 'XG-1295 (X01 12s)', 'XG-1299 (XX1 12s)', 'XS-1275 (Transmission)', 'XS-1295 (Transmission)', 'XS-1299 (Transmission)'],
            'microSHIFT': ['H081 (8s)', 'H092 (9s)', 'H100 (10s)', 'H113 (11s)', 'Advent (9s 11-42/46)', 'Advent X (10s 11-48)', 'Acolyte (8s 12-42/46)'],
            'SunRace': ['CSM90 (9s)', 'CSMS2 (10s)', 'CSMX3 (10s)', 'CSMS8 (11s)', 'CSMX8 (11s)', 'CSMZ80 (12s)', 'CSMZ90 (12s)'],
            'e*thirteen': ['TRS Plus (9-44/9-46)', 'TRS Race (9-46)', 'Helix R (9-46/9-50/9-52)', 'Helix Plus (9-50)'],
            'Garbaruk': ['10s (11-42/45)', '11s (11-46/48/50)', '12s (10-50/52)', '12s Microspline (10-52)'],
            'Box Components': ['Box Four (8s 11-42)', 'Box Three (9s 11-50)', 'Box Two (11s 11-50)', 'Box One (11s 11-50)']
        },
        chain: {
            'Shimano': ['UG51 (6/7/8s)', 'HG40 (6/7/8s)', 'HG71 (8s)', 'HG53 (9s)', 'HG93 (9s)', 'HG54 (10s)', 'HG95 (10s)', 'HG601 (11s)', 'HG701 (11s)', 'HG901 (11s)', 'M6100 (12s)', 'M7100 (12s)', 'M8100 (12s)', 'M9100 (12s)', 'E6090 (E-Bike 10s)', 'E8000 (E-Bike 11s)'],
            'SRAM': ['PC-830', 'PC-850', 'PC-870', 'PC-951', 'PC-971', 'PC-991', 'PC-1031', 'PC-1051', 'PC-1071', 'PC-1091R', 'PC-1110', 'PC-1130', 'PC-1170', 'XX1 11s', 'SX Eagle', 'NX Eagle', 'GX Eagle', 'X01 Eagle', 'XX1 Eagle', 'Flattop Transmission GX', 'Flattop Transmission X0', 'Flattop Transmission XX', 'EX1 (E-Bike)'],
            'KMC': ['Z6', 'Z7', 'Z8', 'Z9', 'X8', 'X9', 'X10', 'X10EL', 'X10SL', 'X11', 'X11EL', 'X11SL', 'X12', 'X12 Ti-N', 'X12 DLC', 'e8 (E-Bike)', 'e9 (E-Bike)', 'e10 (E-Bike)', 'e11 (E-Bike)', 'e12 (E-Bike)'],
            'Connex': ['800', '804', '808', '900', '904', '908', '10s0', '10sB', '10sG', '11s0', '11sB', '11sX', '12s0', '12sX', '10sE (E-Bike)'],
            'YBN': ['S8', 'S9', 'S10', 'S11', 'S12', 'SLA10', 'SLA11', 'SLA12', 'SLA211 (Titanium)', 'SLA212 (Titanium)'],
            'Campagnolo': ['Record 9s', 'Record 10s', 'Record 11s', 'Record 12s', 'Super Record 12s']
        },
        brakes: {
            'Shimano': ['Tourney TX805 (Mech)', 'MT200', 'MT400', 'MT500', 'MT420 (4-Pot)', 'MT520 (4-Pot)', 'Deore M6000', 'Deore M6100', 'Deore M6120 (4-Pot)', 'SLX M7000', 'SLX M7100', 'SLX M7120 (4-Pot)', 'XT M8000', 'XT M8100', 'XT M8120 (4-Pot)', 'XTR M9000', 'XTR M9020', 'XTR M9100', 'XTR M9120 (4-Pot)', 'ZEE M640 (4-Pot)', 'Saint M820 (4-Pot)'],
            'SRAM': ['Level', 'Level T', 'Level TL', 'Level TLM', 'Level Ultimate', 'Level Bronze Stealth', 'Level Silver Stealth', 'Level Ultimate Stealth', 'Guide T', 'Guide R', 'Guide RS', 'Guide RSC', 'Guide Ultimate', 'Guide RE', 'G2 R', 'G2 RS', 'G2 RSC', 'G2 Ultimate', 'Code R', 'Code RS', 'Code RSC', 'Code Bronze Stealth', 'Code Silver Stealth', 'Code Ultimate Stealth', 'Maven Bronze', 'Maven Silver', 'Maven Ultimate'],
            'Magura': ['MT Sport', 'MT2', 'MT4', 'MT5', 'MT5 FABIO WIBMER', 'MT7 Pro', 'MT7 Raceline', 'MT8 Pro', 'MT8 SL', 'MT Trail Sport', 'MT Trail SL'],
            'Hope': ['Tech 3 X2', 'Tech 3 E4', 'Tech 3 V4', 'Tech 4 X2', 'Tech 4 E4', 'Tech 4 V4'],
            'TRP': ['Slate T4', 'Slate EVO', 'Quadiem', 'G-Spec Quadiem', 'Trail EVO', 'DH-R EVO', 'DH-R EVO Gold'],
            'Hayes': ['Radar', 'Prime Sport', 'Prime Pro', 'Dominion A2', 'Dominion A4', 'Dominion T2', 'Dominion T4'],
            'Formula': ['RX', 'The One', 'RO Racing', 'Cura', 'Cura 4', 'Cura X'],
            'Clarks': ['Clout 1', 'M2', 'M3', 'M4'],
            'Tektro': ['Aries (Mech)', 'Aquila (Mech)', 'HD-M275', 'HD-M285', 'Gemini', 'Auriga', 'Orion 4P'],
            'Promax': ['Solve', 'F1', 'Decipher']
        },
        rotors: {
            'Shimano': ['SM-RT10', 'SM-RT26', 'SM-RT30', 'SM-RT54', 'SM-RT56', 'SM-RT64', 'SM-RT66', 'SM-RT70 (Ice-Tech)', 'SM-RT76', 'SM-RT86 (Ice-Tech)', 'RT-MT800 (Ice-Tech Freeza)', 'RT-MT900 (Ice-Tech Freeza)', 'SM-RT99'],
            'SRAM': ['Centerline', 'Centerline 2-Piece', 'Centerline Rounded', 'HS2', 'Paceline', 'G2 CleanSweep'],
            'Hope': ['Standard 6-Bolt', 'Floating 6-Bolt', 'Vented V4', 'Centerlock Floating'],
            'Magura': ['Storm', 'Storm HC', 'Storm SL.2', 'MDR-C', 'MDR-P'],
            'TRP': ['TR-16', 'TR-25', 'TR-29', 'TR-33', 'R1', 'RS01E', 'RS02M'],
            'Galfer': ['Wave Fixed', 'Wave Floating', 'Disc Shark'],
            'Hayes': ['D-Series', 'V-Series'],
            'Formula': ['1-Piece Solid', '1-Piece Lightweight', '2-Piece Floating'],
            'Clarks': ['Wavy', 'Floating'],
            'SwissStop': ['Catalyst One', 'Catalyst Pro', 'Catalyst Race'],
            'AbsoluteBlack': ['Raven']
        },
        wheels: {
            'DT Swiss': ['E 1900 Spline', 'M 1900 Spline', 'X 1900 Spline', 'E 1700 Spline', 'M 1700 Spline', 'X 1700 Spline', 'EX 1700 Spline', 'XM 1700 Spline', 'XR 1700 Spline', 'EX 1501 Spline One', 'XM 1501 Spline One', 'XR 1501 Spline One', 'EXC 1501 Carbon', 'XMC 1501 Carbon', 'XRC 1501 Carbon', 'EXC 1200 Carbon', 'XMC 1200 Carbon', 'XRC 1200 Carbon', 'FR 1950 Classic', 'FR 541', 'HX 1700 (E-Bike)'],
            'Stan\'s NoTubes': ['Crest S1', 'Arch S1', 'Flow S1', 'Crest MK3', 'Arch MK3', 'Flow MK3', 'Crest MK4', 'Arch MK4', 'Flow MK4', 'Flow EX3', 'Crest CB7 Carbon', 'Arch CB7 Carbon', 'Flow CB7 Carbon', 'Podium SRD Carbon'],
            'Industry Nine': ['1/1 Trail S', '1/1 Enduro S', 'Hydra Trail S', 'Hydra Enduro S', 'Hydra Trail 270', 'Hydra Enduro 305', 'Hydra Grade 300', 'Ultralite 235', 'Pillar Carbon Trail', 'Pillar Carbon Enduro'],
            'Crankbrothers': ['Cobalt 1', 'Cobalt 2', 'Cobalt 3', 'Cobalt 11 Carbon', 'Iodine 2', 'Iodine 3', 'Opium 3', 'Synthesis Alloy XCT', 'Synthesis Alloy Enduro', 'Synthesis Alloy DH', 'Synthesis Carbon XCT', 'Synthesis Carbon Enduro', 'Synthesis Carbon DH'],
            'Mavic': ['Crossmax', 'Crossmax SL', 'Crossmax XL', 'Crossmax SL R Carbon', 'Crossmax XL R Carbon', 'Deemax', 'Deemax Park', 'Deemax Pro', 'E-Deemax'],
            'Enve': ['M525', 'M630', 'M635', 'M640', 'M730', 'M735', 'M930', 'Foundation AM30'],
            'Hope': ['Fortus 23', 'Fortus 26', 'Fortus 30', 'Fortus 30 SC', 'Hope Tech 35W'],
            'Race Face': ['Aeffect R', 'Turbine R', 'Atlas', 'Next R Carbon', 'Next SL Carbon'],
            'Hunt': ['Trail Wide', 'Enduro Wide', 'All-Mountain Carbon H_Impact', 'Enduro Carbon H_Impact', 'Proven Race XC', 'Proven Race Enduro'],
            'Spank': ['Spoon 32', 'Spike Race 33', 'Oozy Trail 395+', 'Oozy Trail 345', 'Hex Drive', 'Vibrocore 350'],
            'Reynolds': ['TR 309', 'TR 309 S', 'TR 367', 'TR 367 S', 'Blacklabel XC', 'Blacklabel Trail', 'Blacklabel Enduro'],
            'e*thirteen': ['LG1 Base', 'LG1 Plus', 'LG1 Race Carbon', 'TRS Base', 'TRS Plus', 'TRS Race Carbon', 'XCX Race Carbon'],
            'Roval': ['Traverse Alloy', 'Traverse SL Carbon', 'Control Alloy', 'Control Carbon', 'Control SL Carbon'],
            'Santa Cruz / Reserve': ['Reserve 25', 'Reserve 27', 'Reserve 30', 'Reserve 30|SL', 'Reserve 30|HD', 'Reserve 31|DH', 'Reserve 28|XC'],
            'Bontrager': ['Kovee Comp', 'Kovee Elite', 'Kovee Pro', 'Kovee RSL', 'Line Comp', 'Line Elite', 'Line Pro Carbon', 'Line DH']
        },
        tires: {
            'Maxxis': ['Minion DHF', 'Minion DHR II', 'Assegai', 'High Roller II', 'Shorty', 'Wetscream', 'Aggressor', 'Dissector', 'Forekaster', 'Ardent', 'Ardent Race', 'Ikon', 'Rekon', 'Rekon Race', 'Crossmark II', 'Aspen', 'Severe', 'Tomahawk', 'Griffin', 'Pace', 'Larsen TT', 'Ignitor', 'Minion SS', 'Agressor', 'MaxxLite'],
            'Continental': ['Kryptotal-F', 'Kryptotal-R', 'Argotal', 'Hydrotal', 'Xynotal', 'Der Kaiser', 'Der Baron', 'Mud King', 'Trail King', 'Mountain King', 'Cross King', 'Race King', 'Speed King', 'Ruban', 'Terra Trail'],
            'Schwalbe': ['Magic Mary', 'Big Betty', 'Hans Dampf', 'Nobby Nic', 'Wicked Will', 'Racing Ray', 'Racing Ralph', 'Thunder Burt', 'Rocket Ron', 'Smart Sam', 'Dirty Dan', 'Ice Spiker Pro', 'Eddy Current Front', 'Eddy Current Rear', 'Fat Albert'],
            'Vittoria': ['Mazza', 'Martello', 'Mota', 'Morsa', 'Agarro', 'Barzo', 'Mezcal', 'Gato', 'Synergic', 'E-Mazza', 'E-Martello', 'E-Barzo'],
            'WTB': ['Verdict', 'Verdict Wet', 'Judge', 'Vigilante', 'Trail Boss', 'Ranger', 'Riddler', 'Nano', 'Vulpine', 'Convict', 'Wolverine', 'Breakout'],
            'Michelin': ['Wild Enduro Front', 'Wild Enduro Rear', 'Wild AM', 'Wild AM2', 'Force AM', 'Force AM2', 'Force XC', 'Jet XC2', 'DH22', 'DH34', 'DH Mud', 'E-Wild'],
            'Pirelli': ['Scorpion Race DH M', 'Scorpion Race DH T', 'Scorpion Race DH S', 'Scorpion Race Enduro M', 'Scorpion Race Enduro T', 'Scorpion Race Enduro S', 'Scorpion Enduro S', 'Scorpion Enduro M', 'Scorpion Enduro R', 'Scorpion Trail S', 'Scorpion Trail M', 'Scorpion Trail R', 'Scorpion XC S', 'Scorpion XC M', 'Scorpion XC R', 'Scorpion XC RC'],
            'Specialized': ['Butcher', 'Eliminator', 'Hillbilly', 'Purgatory', 'Ground Control', 'Fast Trak', 'Renegade', 'Slaughter', 'Cannibal'],
            'Bontrager': ['SE6 Team Issue', 'SE5 Team Issue', 'SE4 Team Issue', 'XR4 Team Issue', 'XR3 Team Issue', 'XR2 Team Issue', 'XR1 Team Issue', 'G5 Team Issue', 'G-Mud'],
            'Hutchinson': ['Griffus', 'Toro', 'Kraken', 'Skeleton', 'Taipan', 'Gila', 'Cougar', 'Python 2', 'Skeleton Racing Lab'],
            'Kenda': ['Hellkat Pro', 'Nevegal 2', 'Pinner Pro', 'Regolith Pro', 'Booster Pro', 'Honey Badger', 'Karma 2', 'El Moco', 'Small Block Eight', 'Slant Six'],
            'Onza': ['Aquila', 'Porcupine', 'Porcupine RC', 'Ibex', 'Canis', 'Citius', 'Greina'],
            'Goodyear': ['Newton MTF', 'Newton MTR', 'Escape', 'Peak', 'Connector', 'Wrangler MTF']
        },
        handlebar: {
            'Renthal': ['Fatbar 35', 'Fatbar Carbon 35', 'Fatbar Lite 35', 'Fatbar Lite Carbon 35', 'Fatbar 31.8', 'Fatbar Carbon 31.8', 'Fatbar Lite 31.8', 'Fatbar V2'],
            'Race Face': ['Next 35 Carbon', 'Next R 35 Carbon', 'SixC 35 Carbon', 'Turbine R 35', 'Atlas 35', 'Aeffect R 35', 'Chester 35', 'Respond', 'Evolve'],
            'Deity': ['Skywire 35 Carbon', 'Speedway 35 Carbon', 'Ridgeline 35', 'Racepoint 35', 'Topside 35', 'Blacklabel 31.8', 'Hole Shot 31.8', 'Highside 760', 'Highside 50mm'],
            'Chromag': ['BZA 35 Carbon', 'Cutlass 31.8 Carbon', 'OSX 35', 'OSX 31.8', 'OSX LTD', 'FU40', 'FU50', 'Acute'],
            'OneUp Components': ['Carbon Handlebar 35', 'Aluminum Handlebar 35'],
            'Burgtec': ['Ride Wide Enduro Carbon 35', 'Ride Wide Enduro Alloy 35', 'Ride Wide DH Alloy 35', 'Ride Wide DH Alloy 31.8', 'Josh Bryceland Signature'],
            'Spank': ['Spike 800 Vibrocore', 'Spike 35 Vibrocore', 'Oozy 780 Trail', 'Oozy 35', 'Spoon 800', 'Spoon 785'],
            'e*thirteen': ['Race Carbon 35', 'Plus Alloy 35', 'Base Alloy 35'],
            'Truvativ': ['Descendant Carbon 35', 'Descendant Alloy 35', 'Descendant DH', 'Stylo Carbon', 'Stylo Alloy', 'Jerome Clementz Signature', 'Danny Hart Signature'],
            'Pro (Shimano)': ['Tharsis 35 Carbon', 'Tharsis 31.8 Carbon', 'Koryak Di2', 'Koryak 35', 'LT', 'FRS'],
            'ENVE': ['M5', 'M6', 'M7', 'M9', 'Sweep', 'Riser'],
            'Hope': ['Carbon 35', 'Carbon 31.8'],
            'PNW Components': ['Range Handlebar Gen 3', 'Loam Carbon'],
            'Thomson': ['Elite Carbon', 'Elite Titanium', 'Elite Alloy Trail'],
            'Nukeproof': ['Horizon V2 Carbon', 'Horizon V2 Alloy', 'Sam Hill Signature'],
            'Title': ['AH1 35', 'AH1 31.8', 'Form Carbon']
        },
        stem: {
            'Renthal': ['Apex 35', 'Apex 31.8', 'Integra 35 (Direct Mount)', 'Integra 31.8 (Direct Mount)', 'Strata (Direct Mount)'],
            'Race Face': ['Turbine R 35', 'Atlas 35', 'Atlas 31.8', 'Atlas Direct Mount', 'Aeffect R 35', 'Aeffect 31.8', 'Chester 35', 'Chester Direct Mount', 'Respond'],
            'Deity': ['Copperhead 35', 'Copperhead 31.8', 'Cavity 31.8', 'Micro DM', 'Intake 31.8 DM', 'Intake 35 DM', 'Crosshair'],
            'Hope': ['AM/Freeride 31.8', 'Gravity 35', 'Direct Mount 31.8', 'Direct Mount 35', 'XC 31.8'],
            'Chromag': ['Ranger V2 31.8', 'BZA 35', 'Hifi V2 31.8', 'Hifi 35', 'Director Direct Mount', 'Rift Direct Mount'],
            'Burgtec': ['Enduro MK3 35', 'Enduro MK3 31.8', 'Direct Mount MK3 35', 'Direct Mount MK3 31.8'],
            'Industry Nine': ['A35', 'A318', 'A35 Direct Mount'],
            'OneUp Components': ['Stem 35'],
            'Spank': ['Split 35', 'Split 31.8', 'Spike Race 2', 'Oozy Trail', 'Spike Direct Mount'],
            'Truvativ': ['Descendant 35', 'Descendant 31.8', 'Descendant Direct Mount', 'Stylo', 'Holzfeller', 'Hussefelt'],
            'Thomson': ['Elite X4 31.8', 'Elite 35', 'Direct Mount'],
            'e*thirteen': ['Plus 35', 'Base 35'],
            'Pro (Shimano)': ['Tharsis 35', 'Koryak 35', 'Koryak 31.8', 'LT', 'FRS Direct Mount'],
            'Title': ['ST1 35', 'ST1 31.8', 'DM1 Direct Mount'],
            'PNW Components': ['Range Stem Gen 3'],
            'Nukeproof': ['Horizon', 'Neutron', 'Sam Hill Signature']
        },
        grips: {
            'ODI': ['Ruffian Lock-On', 'Ruffian Mini', 'Elite Pro Lock-On', 'Elite Motion Lock-On', 'Elite Flow Lock-On', 'Rogue Lock-On', 'Oury Lock-On', 'AG-1 Aaron Gwin', 'AG-2 Aaron Gwin', 'Troy Lee Designs Lock-On', 'Vans Lock-On', 'F-1 Float', 'Dreadlocks'],
            'Ergon': ['GE1 Evo', 'GE1 Evo Factory', 'GA2', 'GA2 Fat', 'GA3', 'GD1 Evo', 'GD1 Factory', 'GFR1', 'GFR1 Factory', 'GS1', 'GP1'],
            'DMR': ['Deathgrip', 'Deathgrip Flangeless', 'Deathgrip Thick', 'Brendog', 'Sect'],
            'Race Face': ['Half Nelson', 'Getta Grip', 'Love Handle', 'Grippler', 'Chester'],
            'PNW Components': ['Loam Grip', 'Loam Grip XL'],
            'Deity': ['Knuckleduster', 'Supracush', 'Lockjaw', 'Slimfit', 'Waypoint'],
            'Renthal': ['Lock-On Traction', 'Lock-On Kevlar', 'Lock-On Ultra Tacky', 'Push-On Kevlar', 'Push-On Ultra Tacky'],
            'Chromag': ['Format', 'Squarewaves', 'Basis', 'Wax', 'Clutch', 'Palmskin'],
            'ESI': ['Chunky', 'Extra Chunky', 'Fit SG', 'Fit CR', 'Racer\'s Edge', 'Plush'],
            'Sensus': ['Swayze', 'Lite', 'Meaty Paw', 'Emil Johansson Signature', 'Bite', 'Disisdaboss'],
            'Wolf Tooth': ['Fat Paw', 'Fat Paw Cam', 'Karat', 'Mega Fat Paw', 'Razer', 'Echo Lock-On'],
            'Lizard Skins': ['MacAskill', 'Peaty', 'Northshore', 'Machine', 'Charger', 'Moab', 'DSP 30.3', 'DSP 32.3'],
            'Burgtec': ['Bartender', 'Bartender Pro (Greg Minnaar)'],
            'Spank': ['Spike 30', 'Spike 33', 'Oozy Trail'],
            'OneUp Components': ['Lock-On Grips'],
            'WTB': ['Trail', 'Wafel', 'Commander', 'Koda'],
            'Syncros': ['Pro Lock-On', 'Comfort Lock-On', 'XR Silicon']
        },
        seatpost: {
            'Fox': ['Transfer Factory', 'Transfer Performance Elite', 'Transfer Performance', 'Transfer SL Factory', 'Transfer SL Performance Elite', 'Transfer SL Performance'],
            'RockShox': ['Reverb AXS', 'Reverb Stealth', 'Reverb XPLR AXS'],
            'OneUp Components': ['Dropper Post V2', 'Dropper Post V3'],
            'BikeYoke': ['Revive', 'Revive Max', 'Divine', 'Divine SL', 'Divine SL Rascal'],
            'PNW Components': ['Loam Dropper', 'Ridge Dropper', 'Cascade Dropper', 'Rainier Gen 3', 'Pine Dropper', 'Coast Suspension Dropper'],
            'KS (Kind Shock)': ['LEV Integra', 'LEV Ci', 'LEV Si', 'Rage-i', 'Dropzone', 'Supernatural', 'Crux-i', 'Eten', 'Eten-i'],
            'Crankbrothers': ['Highline 3', 'Highline 7', 'Highline 11 Carbon', 'Highline XC/Gravel'],
            'Race Face': ['Turbine R Dropper', 'Aeffect R Dropper', 'Chester Rigid', 'Next Carbon Rigid'],
            'Thomson': ['Elite Dropper', 'Covert Dropper', 'Elite Rigid', 'Masterpiece Rigid', 'Masterpiece Carbon'],
            'TranzX': ['Kitsuma Air', 'Kitsuma Coil', 'Skyline', 'Jump Seat'],
            'e*thirteen': ['Vario Infinite'],
            'SDG': ['Tellis V2', 'Tellis'],
            'Specialized': ['Command Post IRcc', 'Command Post BlackLite', 'Command Post SRL'],
            'Bontrager': ['Line Elite Dropper', 'Line Dropper', 'Drop Line'],
            'Syncros': ['Duncan Dropper 1.5', 'Duncan Dropper 2.0', 'Duncan Aero'],
            'Hope': ['Carbon Seatpost', 'Eternity']
        },
        saddle: {
            'Ergon': ['SM Pro', 'SM Comp', 'SM Sport', 'SM Enduro Pro', 'SM Enduro Comp', 'SMC Core', 'SR Allroad', 'SR Pro', 'SM E-Mountain'],
            'WTB': ['Volt', 'Silverado', 'Koda', 'Pure', 'Rocket', 'Hightail', 'Devo', 'Gravelier'],
            'Specialized': ['Power Pro', 'Power Expert', 'Power Comp', 'Phenom Pro', 'Phenom Expert', 'Bridge Comp', 'Bridge Sport', 'Romin EVO', 'Henge', 'Avatar'],
            'Fizik': ['Terra Alpaca X5', 'Gravita Alpaca X5', 'Taiga', 'Tundra M3', 'Gobi M3', 'Antares', 'Aliante', 'Vento Argo', 'Tempo Argo'],
            'Selle Italia': ['SLR Boost', 'Flite Boost', 'Model X', 'X-Bow', 'Novus Boost Evo', 'SLR TM Superflow', 'Max Flite'],
            'SDG': ['Bel-Air V3', 'Radar', 'Duster', 'Circuit', 'Fly', 'Apollo', 'Patriot'],
            'Chromag': ['Trailmaster', 'Trailmaster DT', 'Trailmaster LTD', 'Lynx DT', 'Moon', 'Overture', 'Mood'],
            'Fabric': ['Scoop Shallow', 'Scoop Radius', 'Scoop Flat', 'Line Shallow', 'Line Pro', 'Cell', 'Magic', 'Alm'],
            'Prologo': ['Dimension NDR', 'Dimension Space', 'Scratch M5', 'Scratch X8', 'Nago X10', 'Proxim W450', 'Proxim W650 (E-Bike)'],
            'SQLab': ['611 Ergowave', '611 Ergowave Active', '612 Ergowave', '60X Ergowave', '6OX Infinergy'],
            'Bontrager': ['Arvada', 'Verse', 'Aeolus', 'Kovee', 'Montrose', 'Ajna', 'Evoke'],
            'Syncros': ['Tofino', 'Savona', 'Belcarra', 'Comox', 'Capilano'],
            'Tioga': ['Spyder Outland', 'Spyder Stratum', 'Undercover Stratum', 'D-Spyder'],
            'Selle San Marco': ['Ground', 'Allroad', 'Shortfit', 'Aspide', 'Mantra'],
            'Deity': ['Speedtrap', 'Sidetrack', 'Frisco']
        },
        pedals: {
            'Shimano': ['PD-M9120 (XTR Trail)', 'PD-M9100 (XTR XC)', 'PD-M8120 (XT Trail)', 'PD-M8100 (XT XC)', 'PD-M8140 (XT Flat)', 'PD-M828 (Saint Flat)', 'PD-M820 (Saint Clipless)', 'PD-M821 (Saint Clipless)', 'PD-M647 (DX)', 'PD-M642 (ZEE Flat)', 'PD-M540', 'PD-M530', 'PD-M520', 'PD-M424', 'PD-M324', 'PD-GR500 (Flat)', 'PD-GR400 (Flat)', 'PD-EF202 (Flat)', 'PD-EH500 (Hybrid)'],
            'Crankbrothers': ['Mallet E', 'Mallet E LS', 'Mallet DH', 'Mallet 2', 'Mallet 3', 'Eggbeater 11', 'Eggbeater 3', 'Eggbeater 2', 'Eggbeater 1', 'Candy 11', 'Candy 7', 'Candy 3', 'Candy 2', 'Candy 1', 'Stamp 1 (Flat)', 'Stamp 2 (Flat)', 'Stamp 3 (Flat)', 'Stamp 7 (Flat)', 'Stamp 11 (Flat)', 'Double Shot 1', 'Double Shot 2', 'Double Shot 3'],
            'Race Face': ['Atlas', 'Aeffect', 'Chester', 'Ride'],
            'Deity': ['TMAC', 'Bladerunner', 'Black Kat', 'Deftrap', 'Compound'],
            'HT Components': ['X2 (DH Clipless)', 'X2T (Titanium)', 'T1 (Enduro Clipless)', 'T2', 'ME03 (Magnesium Flat)', 'AE03 (Evo Flat)', 'AE05', 'ANS10 Supreme', 'PA03A (Composite Flat)', 'Leopard M4'],
            'Hope': ['F20', 'F22', 'Union TC', 'Union GC', 'Union RC'],
            'Burgtec': ['Penthouse Flat MK5', 'Penthouse Flat MK5 Composite', 'MK4'],
            'OneUp Components': ['Aluminum Pedals', 'Composite Pedals'],
            'DMR': ['Vault', 'Vault Midi', 'Vault Mag', 'V12', 'V12 Mag', 'V11 (Composite)', 'V8', 'V6'],
            'Nukeproof': ['Horizon Pro', 'Horizon Comp', 'Horizon CS Trail', 'Horizon CL DH', 'Neutron Evo'],
            'Look': ['X-Track Race Carbon Ti', 'X-Track Race Carbon', 'X-Track Race', 'X-Track En-Rage', 'X-Track En-Rage Plus', 'Trail Roc (Flat)', 'Trail Grip'],
            'Spank': ['Oozy Trail', 'Spike Reboot', 'Spoon 110', 'Spoon 100', 'Spoon 90'],
            'Time': ['Speciale 12', 'Speciale 8', 'ATAC XC 12', 'ATAC XC 8', 'ATAC XC 6', 'ATAC MX 6', 'ATAC MX 4'],
            'Chromag': ['Scarab', 'Dagga', 'Contact', 'Synth'],
            'Yoshimura': ['Chilao'],
            'Bontrager': ['Line Pro', 'Line Elite', 'Elite MTB Clipless', 'Comp MTB Clipless']
        }
    };


    // Hangi adımda dropdown yok → serbest metin
    const FREETEXT_STEPS = new Set(['extras']);

    // =========================================================
    // DROPDOWN UI OLUŞTURUCUSU (CUSTOM BUILD)
    // =========================================================
    window.renderBuildInputUI = function() {
        const step = BUILD_STEPS[currentBuildStepIndex];
        if (!step) return;
        const isFree = FREETEXT_STEPS.has(step.id) || !PARTS_DB[step.id];
        const area = document.getElementById('ai-build-input-area');
        if (!area) return;

        if (isFree) {
            area.innerHTML = `
                <input type="text" id="ai-inp-build" class="ai-input mb-3" placeholder="Marka ve model girin...">
                <div class="flex gap-2 mb-4">
                    <button class="flex-[2] ai-btn bg-purple-600 hover:bg-purple-500 text-white !border-none" onclick="runAI('build')" style="pointer-events:auto;">Ekle &amp; Kontrol Et</button>
                    <button class="flex-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-xl text-xs font-bold transition-all" onclick="window.aiSkipBuildStep()" style="pointer-events:auto;">Geç ⏭</button>
                    <button class="flex-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-xl text-xs font-bold transition-all" onclick="window.aiUndoBuildStep()" style="pointer-events:auto;">← Geri Al</button>
                </div>
            `;
        } else {
            const brands = Object.keys(PARTS_DB[step.id]).sort();
            const brandOptions = brands.map(b => `<option value="${b}">${b}</option>`).join('');
            area.innerHTML = `
                <div class="flex flex-col gap-2 mb-3">
                    <select id="ai-build-brand" onchange="window.onBuildBrandChange()" class="w-full bg-zinc-900 border border-zinc-700 text-white rounded-xl px-3 py-2.5 text-sm font-semibold focus:outline-none focus:border-purple-500 transition-colors">
                        <option value="">— Marka Seç —</option>
                        ${brandOptions}
                    </select>
                    <select id="ai-build-model" class="w-full bg-zinc-900 border border-zinc-700 text-white rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:border-purple-500 transition-colors" disabled>
                        <option value="">— Önce marka seçin —</option>
                    </select>
                    <div id="ai-build-selected-preview" class="hidden text-xs text-purple-300 font-bold bg-purple-900/20 border border-purple-700/40 rounded-lg px-3 py-2"></div>
                    <div class="text-center text-zinc-500 text-xs font-bold my-1">— VEYA —</div>
                    <input type="text" id="ai-inp-build" class="ai-input mt-1" placeholder="Listede yoksa direkt yazın..." oninput="window.onBuildManualInput()">
                </div>
                <div class="flex gap-2 mb-4">
                    <button class="flex-[2] ai-btn bg-purple-600 hover:bg-purple-500 text-white !border-none" onclick="runAI('build')" style="pointer-events:auto;">Ekle &amp; Kontrol Et</button>
                    <button class="flex-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-xl text-xs font-bold transition-all" onclick="window.aiSkipBuildStep()" style="pointer-events:auto;">Geç ⏭</button>
                    <button class="flex-1 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-xl text-xs font-bold transition-all" onclick="window.aiUndoBuildStep()" style="pointer-events:auto;">← Geri Al</button>
                </div>
            `;
        }
    };

    window.onBuildBrandChange = function() {
        const step = BUILD_STEPS[currentBuildStepIndex];
        const brand = document.getElementById('ai-build-brand').value;
        const modelSel = document.getElementById('ai-build-model');
        const preview = document.getElementById('ai-build-selected-preview');
        const inp = document.getElementById('ai-inp-build');
        if (!brand) { modelSel.disabled = true; modelSel.innerHTML = '<option>— Önce marka seçin —</option>'; preview.classList.add('hidden'); inp.value = ''; return; }
        const models = PARTS_DB[step.id][brand] || [];
        modelSel.disabled = false;
        modelSel.innerHTML = '<option value="">— Model Seç —</option>' + models.map(m => `<option value="${m}">${m}</option>`).join('');
        modelSel.onchange = function() {
            const model = modelSel.value;
            if (model) {
                inp.value = brand + ' ' + model;
                preview.textContent = '✅ Seçilen: ' + brand + ' ' + model;
                preview.classList.remove('hidden');
            } else {
                inp.value = '';
                preview.classList.add('hidden');
            }
        };
        inp.value = ''; preview.classList.add('hidden');
    };

    window.onBuildManualInput = function() {
        const inp = document.getElementById('ai-inp-build').value;
        const preview = document.getElementById('ai-build-selected-preview');
        const brandSel = document.getElementById('ai-build-brand');
        const modelSel = document.getElementById('ai-build-model');
        if (inp) {
            if (preview) { preview.textContent = '✏️ Manuel giriş: ' + inp; preview.classList.remove('hidden'); }
            if (brandSel) { brandSel.value = ''; }
            if (modelSel) { modelSel.innerHTML = '<option>— Önce marka seçin —</option>'; modelSel.disabled = true; }
        } else {
            if (preview) preview.classList.add('hidden');
        }
    };

    // =========================================================
    // DROPDOWN UI OLUŞTURUCUSU (PARÇA İNCELEME)
    // =========================================================
    window.renderPartInputUI = function() {
        const categories = Object.keys(PARTS_DB);
        const catMap = {
            frame: 'Kadro', headset: 'Furç Takımı', fork: 'Maşa', shock: 'Arka Şok', bb: 'Orta Göbek', crank: 'Aynakol',
            chainguide: 'Zincir Gergisi', derailleur: 'Arka Aktarıcı', shifter: 'Vites Kolu', cassette: 'Kaset',
            chain: 'Zincir', brakes: 'Fren Seti', rotors: 'Fren Diskleri', wheels: 'Jant Seti', tires: 'Lastikler',
            handlebar: 'Gidon', stem: 'Gidon Boğazı', grips: 'Elcik', seatpost: 'Sele Borusu', saddle: 'Sele', pedals: 'Pedallar'
        };
        const catOptions = categories.map(c => `<option value="${c}">${catMap[c] || c}</option>`).join('');

        const html = `
            <div class="flex flex-col gap-2 mb-4">
                <select id="ai-part-cat" onchange="window.onPartCatChange()" class="w-full bg-zinc-900 border border-zinc-700 text-white rounded-xl px-3 py-2.5 text-sm font-semibold focus:outline-none focus:border-blue-500 transition-colors">
                    <option value="">— Parça Türü Seç —</option>
                    ${catOptions}
                </select>
                <select id="ai-part-brand" onchange="window.onPartBrandChange()" class="w-full bg-zinc-900 border border-zinc-700 text-white rounded-xl px-3 py-2.5 text-sm font-semibold focus:outline-none focus:border-blue-500 transition-colors" disabled>
                    <option value="">— Önce tür seçin —</option>
                </select>
                <select id="ai-part-model" class="w-full bg-zinc-900 border border-zinc-700 text-white rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:border-blue-500 transition-colors" disabled>
                    <option value="">— Önce marka seçin —</option>
                </select>
                <div id="ai-part-selected-preview" class="hidden text-xs text-blue-300 font-bold bg-blue-900/20 border border-blue-700/40 rounded-lg px-3 py-2"></div>
                
                <div class="text-center text-zinc-500 text-xs font-bold my-1">— VEYA —</div>
                <input type="text" id="ai-inp-part" class="ai-input" placeholder="Listede yoksa manuel girin (Örn: Fox 40 Factory)" oninput="window.onPartManualInput()">
            </div>
            <button class="ai-btn bg-blue-600 hover:bg-blue-500 text-white w-full py-3 rounded-xl font-bold transition-all !border-none" onclick="runAI('part')" style="pointer-events: auto;">Skorla & İncele</button>
        `;
        
        const container = document.getElementById('ai-part-input-container');
        if (container) container.innerHTML = html;
    };

    window.onPartCatChange = function() {
        const cat = document.getElementById('ai-part-cat').value;
        const brandSel = document.getElementById('ai-part-brand');
        const modelSel = document.getElementById('ai-part-model');
        const preview = document.getElementById('ai-part-selected-preview');
        const inp = document.getElementById('ai-inp-part');

        if (!cat) {
            brandSel.disabled = true; brandSel.innerHTML = '<option>— Önce tür seçin —</option>';
            modelSel.disabled = true; modelSel.innerHTML = '<option>— Önce marka seçin —</option>';
            preview.classList.add('hidden'); inp.value = ''; return;
        }

        const brands = Object.keys(PARTS_DB[cat]).sort();
        brandSel.disabled = false;
        brandSel.innerHTML = '<option value="">— Marka Seç —</option>' + brands.map(b => `<option value="${b}">${b}</option>`).join('');
        modelSel.disabled = true; modelSel.innerHTML = '<option value="">— Önce marka seçin —</option>';
        inp.value = ''; preview.classList.add('hidden');
    };

    window.onPartBrandChange = function() {
        const cat = document.getElementById('ai-part-cat').value;
        const brand = document.getElementById('ai-part-brand').value;
        const modelSel = document.getElementById('ai-part-model');
        const preview = document.getElementById('ai-part-selected-preview');
        const inp = document.getElementById('ai-inp-part');

        if (!brand) { modelSel.disabled = true; modelSel.innerHTML = '<option>— Önce marka seçin —</option>'; preview.classList.add('hidden'); inp.value = ''; return; }

        const models = PARTS_DB[cat][brand] || [];
        modelSel.disabled = false;
        modelSel.innerHTML = '<option value="">— Model Seç —</option>' + models.map(m => `<option value="${m}">${m}</option>`).join('');
        modelSel.onchange = function() {
            const model = modelSel.value;
            if (model) {
                inp.value = brand + ' ' + model;
                preview.textContent = '✅ Seçilen: ' + brand + ' ' + model;
                preview.classList.remove('hidden');
            } else {
                inp.value = '';
                preview.classList.add('hidden');
            }
        };
        inp.value = ''; preview.classList.add('hidden');
    };

    window.onPartManualInput = function() {
        const inp = document.getElementById('ai-inp-part').value;
        const preview = document.getElementById('ai-part-selected-preview');
        const catSel = document.getElementById('ai-part-cat');
        const brandSel = document.getElementById('ai-part-brand');
        const modelSel = document.getElementById('ai-part-model');

        if (inp) {
            if (preview) { preview.textContent = '✏️ Manuel giriş: ' + inp; preview.classList.remove('hidden'); }
            if (catSel) catSel.value = '';
            if (brandSel) { brandSel.innerHTML = '<option>— Önce tür seçin —</option>'; brandSel.disabled = true; }
            if (modelSel) { modelSel.innerHTML = '<option>— Önce marka seçin —</option>'; modelSel.disabled = true; }
        } else {
            if (preview) preview.classList.add('hidden');
        }
    };

    let currentBuildStepIndex = 0;
    let aiBuildMemory = {};

    window.openAIHub = function() {
        try {
            if(typeof showToast==='function') showToast("AI Hub Açılıyor...", "info", 1500);
            const overlay = document.getElementById('ai-hub-overlay');
            if(!overlay) return;
            document.body.appendChild(overlay);
            overlay.style.setProperty('display', 'flex', 'important');
            overlay.style.setProperty('opacity', '1', 'important');
            overlay.style.setProperty('visibility', 'visible', 'important');
            overlay.style.setProperty('z-index', '9999999', 'important');
            overlay.style.setProperty('pointer-events', 'auto', 'important');
            overlay.style.setProperty('position', 'fixed', 'important');
            overlay.style.setProperty('top', '0', 'important');
            overlay.style.setProperty('left', '0', 'important');
            overlay.style.setProperty('width', '100%', 'important');
            overlay.style.setProperty('height', '100%', 'important');
            overlay.classList.add('show');
            if(typeof window.backToAIMenu === 'function') window.backToAIMenu();
            window.updateBuildProgress(0); // Initialize build UI
        } catch(e) {}
    };

    window.closeAIHub = function() {
        try {
            const overlay = document.getElementById('ai-hub-overlay');
            if(overlay) {
                overlay.classList.remove('show');
                overlay.style.display = 'none';
            }
        } catch(e) {}
    };

    window.backToAIMenu = function() {
        try {
            document.getElementById('ai-main-menu').style.display = 'block';
            document.querySelectorAll('.ai-screen').forEach(el => el.style.display = 'none');
            document.getElementById('ai-hub-title').innerText = 'AI Merkezi';
        } catch(e) {}
    };

    window.openAIScreen = function(type) {
        document.getElementById('ai-main-menu').style.display = 'none';
        document.querySelectorAll('.ai-screen').forEach(el => el.style.display = 'none');
        document.getElementById(`ai-screen-${type}`).style.display = 'flex';
        const titles = { 'analysis': 'Bisiklet Analizi', 'recommend': 'Akıllı Öneri', 'build': 'Custom Build', 'part': 'Parça İnceleme' };
        document.getElementById('ai-hub-title').innerText = titles[type];
        
        // Eğer Custom Build açılıyorsa, UI'ı güncelle
        if (type === 'build') {
            window.updateBuildProgress();
        }
        // Eğer Parça İnceleme açılıyorsa ve dropdown div'i henüz oluşturulmadıysa doldur
        if (type === 'part') {
            const container = document.getElementById('ai-part-input-container');
            // Check if it already has the select elements, if not render it
            if (container && !container.querySelector('select')) {
                window.renderPartInputUI();
            }
        }
    };

    window.updateBuildProgress = function(forceStepIndex = -1) {
        if(forceStepIndex !== -1) currentBuildStepIndex = forceStepIndex;
        
        const isDone = currentBuildStepIndex >= BUILD_STEPS.length;
        
        const progContainer = document.getElementById('ai-build-progress');
        if(progContainer) {
            let dots = '';
            for(let i=0; i<BUILD_STEPS.length; i++) {
                const stepId = BUILD_STEPS[i].id;
                const isInstalled = (i < currentBuildStepIndex);
                
                const svgs = [
                    document.getElementById(`svg-part-${stepId}`),
                    document.getElementById(`svg-part-${stepId}-r`)
                ];
                svgs.forEach(svgEl => {
                    if (svgEl) {
                        if (isInstalled) svgEl.classList.add('svg-installed');
                        else svgEl.classList.remove('svg-installed');
                    }
                });

                if(i < currentBuildStepIndex) dots += '<div class="w-3 h-3 rounded-full bg-green-500 shrink-0"></div>';
                else if(i === currentBuildStepIndex) dots += '<div class="w-3 h-3 rounded-full bg-purple-500 shrink-0 border-2 border-white "></div>';
                else dots += '<div class="w-3 h-3 rounded-full bg-zinc-800 shrink-0"></div>';
            }
            progContainer.innerHTML = dots;
        }

        if(currentBuildStepIndex >= BUILD_STEPS.length) {
            document.getElementById('ai-build-input-area').style.display = 'none';
            document.getElementById('ai-build-complete-area').style.display = 'block';
            document.getElementById('ai-build-step-title').innerText = `${BUILD_STEPS.length} Parça Seçildi`;
            document.getElementById('ai-build-step-counter').innerText = 'Tebrikler';
            document.getElementById('ai-build-summary-text').innerText = 'Tüm donanımlar hazır. Şimdi analiz et veya kopyala.';
        } else {
            document.getElementById('ai-build-input-area').style.display = 'block';
            const step = BUILD_STEPS[currentBuildStepIndex];
            document.getElementById('ai-build-step-counter').innerText = `Adım ${currentBuildStepIndex + 1} / ${BUILD_STEPS.length}`;
            document.getElementById('ai-build-step-title').innerText = step.name;
            const hasDB = PARTS_DB[step.id];
            document.getElementById('ai-build-summary-text').innerText = hasDB ? '⬇️ Listeden seçin veya direkt yazın.' : 'Marka ve model girin.';
            document.getElementById('ai-build-input-area').classList.remove('hidden');
            document.getElementById('ai-build-complete-area').classList.add('hidden');
            window.renderBuildInputUI();
        }
    };

    window.aiUndoBuildStep = function() {
        if(currentBuildStepIndex > 0) {
            currentBuildStepIndex--;
            const stepId = BUILD_STEPS[currentBuildStepIndex].id;
            delete aiBuildMemory[stepId];
            window.updateBuildProgress();
            document.getElementById('ai-res-build').innerHTML = '';
        }
    };

    window.aiSkipBuildStep = function() {
        if(currentBuildStepIndex < BUILD_STEPS.length) {
            const stepId = BUILD_STEPS[currentBuildStepIndex].id;
            aiBuildMemory[stepId] = 'Atlandı / Kullanılmıyor';
            currentBuildStepIndex++;
            window.updateBuildProgress();
            document.getElementById('ai-res-build').innerHTML = `<div class="p-2 bg-zinc-800/80 rounded-lg text-center text-xs text-zinc-400 font-bold border border-zinc-700/50">⏭ Adım atlandı.</div>`;
            document.getElementById('ai-inp-build').value = '';
        }
    };

    window.aiResetBuild = function() {
        aiBuildMemory = {};
        currentBuildStepIndex = 0;
        document.getElementById('ai-res-build').innerHTML = '';
        window.updateBuildProgress();
    };

    window.aiCopyBuild = function() {
        let text = "🚲 Benim Custom Build Projem:\\n";
        for(let i=0; i<BUILD_STEPS.length; i++) {
            const step = BUILD_STEPS[i];
            const part = aiBuildMemory[step.id] || '-';
            text += `✅ ${step.name}: ${part}\\n`;
        }
        navigator.clipboard.writeText(text).then(() => {
            if(typeof showToast==='function') showToast("Tasarım kopyalandı!", "success");
        });
    };

    window.aiAnalyzeFullBuild = async function() {
        const loader = document.getElementById(`ai-loader-build`);
        const resBox = document.getElementById(`ai-res-build`);
        loader.style.display = 'block';
        resBox.innerHTML = '';
        
        try {
            const r = await fetch('/api/data', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: 'ai_bike_build_final', data: { build_data: aiBuildMemory } })
            });
            const data = await r.json();
            loader.style.display = 'none';
            if (data.status === 'error') {
                resBox.innerHTML = `<div class="ai-result-box" style="border-color: #ef4444;"><div class="text-red-400 font-bold">${data.message}</div></div>`;
                return;
            }
            const d = data.data;
            resBox.innerHTML = `<div class="ai-result-box">
                <div class="ai-score-ring">${d.score || 0}</div>
                <div class="text-center text-xs text-zinc-400 mb-6 font-bold tracking-widest uppercase">Genel Uyum Skoru</div>
                <div class="ai-stat-row"><span class="ai-stat-label">Uygun Kategori</span> <span class="ai-stat-val text-purple-400">${d.category || '-'}</span></div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-green-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Genel Değerlendirme</div>
                <div class="text-sm text-zinc-200 leading-relaxed mb-4">${d.overall_review || '-'}</div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-red-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Zayıf Halka / Eksikler</div>
                <ul class="text-zinc-300 text-sm list-disc pl-4 space-y-1">${(d.weaknesses||[]).map(s => `<li>${s}</li>`).join('')}</ul>
                
                <div class="mt-4 mb-2 font-bold text-sm text-yellow-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Tavsiyeler</div>
                <ul class="text-zinc-300 text-sm list-disc pl-4 space-y-1">${(d.recommendations||[]).map(s => `<li>${s}</li>`).join('')}</ul>
            </div>`;
        } catch(e) {
            loader.style.display = 'none';
            resBox.innerHTML = `<div class="ai-result-box" style="border-color: #ef4444;"><div class="text-red-400 font-bold">Analiz hatası oluştu.</div></div>`;
        }
    };

    window.runAI = async function(type) {
        const loader = document.getElementById(`ai-loader-${type}`);
        const resBox = document.getElementById(`ai-res-${type}`);
        loader.style.display = 'block';
        resBox.innerHTML = '';
        
        let payload = { action: '' };
        
        if (type === 'analysis') {
            const val = document.getElementById('ai-inp-analysis').value;
            if(!val) return loader.style.display = 'none';
            payload = { action: 'ai_bike_analysis', data: { bike_info: val } };
        } 
        else if (type === 'recommend') {
            const b = document.getElementById('ai-inp-rec-budget').value;
            const s = document.getElementById('ai-inp-rec-style').value;
            const t = document.getElementById('ai-inp-rec-terrain').value;
            const l = document.getElementById('ai-inp-rec-level').value;
            if(!b || !s) return loader.style.display = 'none';
            payload = { action: 'ai_bike_recommendation', data: { budget: b, style: s, terrain: t, level: l } };
        }
        else if (type === 'build') {
            const req = document.getElementById('ai-inp-build').value;
            if(!req) return loader.style.display = 'none';
            
            const currentStepDef = BUILD_STEPS[currentBuildStepIndex];
            payload = { 
                action: 'ai_bike_build', 
                data: { 
                    history: aiBuildMemory, 
                    new_request: req,
                    current_step: currentStepDef.name,
                    next_step: (currentBuildStepIndex + 1 < BUILD_STEPS.length) ? BUILD_STEPS[currentBuildStepIndex + 1].name : "Tamamlandı"
                } 
            };
        }
        else if (type === 'part') {
            const p = document.getElementById('ai-inp-part').value;
            if(!p) return loader.style.display = 'none';
            payload = { action: 'ai_part_analysis', data: { part_name: p } };
        }
        
        try {
            const r = await fetch('/api/data', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            const data = await r.json();
            loader.style.display = 'none';
            
            if (data.status === 'error') {
                resBox.innerHTML = `<div class="ai-result-box" style="border-color: #ef4444;"><div class="text-red-400 font-bold">${data.message}</div></div>`;
                return;
            }
            
            const d = data.data;
            let html = '';
            
            if (d.status === 'needs_info') {
                html += `<div class="ai-result-box" style="border-color: #eab308; box-shadow: 0 0 15px rgba(234,179,8,0.2);">
                    <div class="text-yellow-400 font-bold mb-2 uppercase tracking-widest text-sm">Eksik Bilgi Tespit Edildi</div>
                    <div class="text-zinc-200 text-sm leading-relaxed">${d.question || 'Lütfen daha detaylı bilgi verin.'}</div>
                </div>`;
                resBox.innerHTML = html;
                return;
            }
            
            if (type === 'analysis') {
                html += `<div class="ai-result-box">
                    <div class="ai-score-ring">${d.performance_score || 0}</div>
                    <div class="text-center text-xs text-zinc-400 mb-6 font-bold tracking-widest uppercase">Performans Skoru</div>
                    
                    <div class="ai-stat-row"><span class="ai-stat-label">Kategori</span> <span class="ai-stat-val text-purple-400">${d.category || '-'}</span></div>
                    <div class="ai-stat-row"><span class="ai-stat-label">Sürüş Tarzı</span> <span class="ai-stat-val">${d.riding_style || '-'}</span></div>
                    <div class="ai-stat-row"><span class="ai-stat-label">Geometri</span> <span class="ai-stat-val">${d.geometry || '-'}</span></div>
                    <div class="ai-stat-row"><span class="ai-stat-label">Süspansiyon</span> <span class="ai-stat-val">${d.suspension || '-'}</span></div>
                    <div class="ai-stat-row"><span class="ai-stat-label">Lastikler</span> <span class="ai-stat-val">${d.tires || '-'}</span></div>
                    
                    <div class="mt-4 mb-2 font-bold text-sm text-green-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Güçlü Yönler</div>
                    <div>${(d.strengths||[]).map(s => `<span class="ai-tag green">${s}</span>`).join('')}</div>
                    
                    <div class="mt-4 mb-2 font-bold text-sm text-red-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Zayıf Yönler</div>
                    <div>${(d.weaknesses||[]).map(s => `<span class="ai-tag red">${s}</span>`).join('')}</div>
                    
                    <div class="mt-4 mb-2 font-bold text-sm text-yellow-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Yükseltme Önerileri</div>
                    <ul class="text-zinc-300 text-sm list-disc pl-4 space-y-1">${(d.upgrades||[]).map(s => `<li>${s}</li>`).join('')}</ul>
                </div>`;
            }
            else if (type === 'recommend') {
                html += `<div class="ai-result-box">
                    <div class="text-center mb-6">
                        <div class="text-3xl mb-2">🚲</div>
                        <div class="font-black text-xl text-purple-400 uppercase tracking-wider">${d.bike_type || '-'}</div>
                        <div class="text-sm font-bold text-green-400 mt-1">${d.estimated_price || 'Bütçe Analizi Yapılmadı'}</div>
                        <div class="text-xs text-zinc-400 mt-2">${d.level_advice || ''}</div>
                    </div>
                    
                    <div class="ai-stat-row"><span class="ai-stat-label">Geometri</span> <span class="ai-stat-val text-blue-300">${d.geometry || '-'}</span></div>
                    <div class="ai-stat-row"><span class="ai-stat-label">Travel Önerisi</span> <span class="ai-stat-val text-yellow-400">${d.suspension_travel || '-'}</span></div>
                    <div class="ai-stat-row"><span class="ai-stat-label">Teker Önerisi</span> <span class="ai-stat-val">${d.wheel_size || '-'}</span></div>
                    
                    <div class="mt-6 mb-2 font-bold text-sm text-white uppercase tracking-widest border-b border-zinc-800 pb-1">Örnek Modeller</div>
                    <div class="flex flex-col gap-2 mt-3">
                        ${(d.models||[]).map(s => `<div class="bg-black/50 border border-zinc-700/50 p-3 rounded-lg font-bold text-sm text-zinc-200 border-l-4 border-l-purple-500">${s}</div>`).join('')}
                    </div>
                </div>`;
            }
            else if (type === 'build') {
                // Save the approved part
                const currentStepDef = BUILD_STEPS[currentBuildStepIndex];
                aiBuildMemory[currentStepDef.id] = document.getElementById('ai-inp-build').value;
                document.getElementById('ai-inp-build').value = '';
                
                // Advance step
                currentBuildStepIndex++;
                window.updateBuildProgress();
                
                let warnHtml = '';
                if (d.compatibility_warning && d.compatibility_warning.length > 5) {
                    warnHtml = `<div class="bg-red-900/30 border-l-4 border-l-red-500 text-red-200 p-2 rounded-r-lg mb-2 text-xs font-medium">⚠️ ${d.compatibility_warning}</div>`;
                }
                
                html += `<div class="bg-black/60 border border-zinc-700/50 rounded-xl p-3  ">
                    ${warnHtml}
                    <div class="flex items-start gap-2">
                        <div class="text-green-500 mt-0.5 text-sm">✅</div>
                        <div class="flex-1">
                            <div class="text-xs text-zinc-300 leading-tight mb-2">${d.compatibility || '-'}</div>
                            <div class="text-[10px] text-purple-400 font-black uppercase tracking-widest mb-1">Sıradaki Adım Önerileri:</div>
                            <ul class="text-[11px] text-zinc-400 list-disc pl-4 space-y-0.5">
                                ${(d.suggestions||[]).map(s => `<li>${s}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                </div>`;
            }
            else if (type === 'part') {
                html += `<div class="ai-result-box">
                    <div class="ai-score-ring" style="border-color:#38bdf8; box-shadow:0 0 20px rgba(56,189,248,0.5)">${d.performance_score || 0}</div>
                    <div class="text-center text-xs text-zinc-400 mb-6 font-bold tracking-widest uppercase">Parça Skoru</div>
                    
                    <div class="ai-stat-row"><span class="ai-stat-label">Kategori</span> <span class="ai-stat-val text-blue-400">${d.category || '-'}</span></div>
                    <div class="ai-stat-row"><span class="ai-stat-label">Seviye</span> <span class="ai-stat-val">${d.level || '-'}</span></div>
                    <div class="ai-stat-row"><span class="ai-stat-label">Sertlik</span> <span class="ai-stat-val">${d.stiffness || '-'}</span></div>
                    <div class="ai-stat-row"><span class="ai-stat-label">Dayanıklılık</span> <span class="ai-stat-val">${d.durability || '-'}</span></div>
                    <div class="ai-stat-row"><span class="ai-stat-label">Fiyat/Performans</span> <span class="ai-stat-val text-green-400">${d.price_performance || '-'}</span></div>
                    
                    <div class="mt-4 mb-2 font-bold text-sm text-green-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Güçlü Yönler</div>
                    <div>${(d.strengths||[]).map(s => `<span class="ai-tag green">${s}</span>`).join('')}</div>
                    
                    <div class="mt-4 mb-2 font-bold text-sm text-red-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Zayıf Yönler</div>
                    <div>${(d.weaknesses||[]).map(s => `<span class="ai-tag red">${s}</span>`).join('')}</div>
                    
                    <div class="mt-4 p-3 bg-blue-900/20 border border-blue-500/30 rounded-lg text-sm text-blue-200 leading-relaxed">
                        <b>💡 Tavsiye:</b> ${d.usage_advice || '-'}
                    </div>
                </div>`;
            }
            
            resBox.innerHTML = html;
            
        } catch(e) {
            loader.style.display = 'none';
            resBox.innerHTML = `<div class="ai-result-box" style="border-color: #ef4444;"><div class="text-red-400 font-bold">Bağlantı hatası oluştu.</div></div>`;
        }
    };

    console.log("AI HUB IIFE loaded successfully.");
})();
