-- Database schema for echo reports
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Patient Info
    patient_name TEXT,
    mrn TEXT,
    dob TEXT,
    gender TEXT,
    
    -- Scan Details
    scan_indication TEXT,
    scan_quality TEXT,
    quality_comments TEXT,
    
    -- Views Obtained
    view_psax BOOLEAN,
    view_plax BOOLEAN,
    view_a4c BOOLEAN,
    view_a5c BOOLEAN,
    view_subx BOOLEAN,
    
    -- Ventricular Assessment
    lv_size TEXT,
    lvidd REAL,
    lv_function TEXT,
    wall_motion_abnormality BOOLEAN,
    rv_size TEXT,
    rv_function TEXT,
    tapse REAL,
    
    -- Septum
    septum_shape TEXT,
    
    -- Valve Assessment
    av_status TEXT,
    mv_status TEXT,
    tv_status TEXT,
    
    -- Other Findings
    aortic_root TEXT,
    ivc TEXT,
    pericardial_fluid TEXT,
    pleural_effusion TEXT,
    additional_observations TEXT,
    
    -- Conclusions
    clinical_conclusion TEXT,
    requires_level2 BOOLEAN,
    physician_informed BOOLEAN,
    
    -- Training Details
    training_approval TEXT,
    reporter_name TEXT,
    training_status TEXT
);