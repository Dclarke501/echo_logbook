import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QTabWidget, QPushButton, QLabel, QLineEdit, 
                            QRadioButton, QButtonGroup, QScrollArea, QGridLayout,
                            QDateEdit, QGroupBox, QHBoxLayout, QCheckBox, QTextEdit)
from PyQt6.QtCore import Qt, QDate
from db_manager import DatabaseManager

class EchoReportApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.db = DatabaseManager()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle("Level 1 Echo Report")
        self.setMinimumSize(1000, 800)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Create and add tabs
        self.create_scan_quality_tab()
        self.create_patient_info_tab()
        self.create_ventricular_tab()
        self.create_valve_tab()
        self.create_other_findings_tab()
        self.create_conclusions_tab()

        # Add save button at the bottom
        save_button = QPushButton("Save Report")
        save_button.clicked.connect(self.save_report)
        main_layout.addWidget(save_button)

    def create_scan_quality_tab(self):
        scan_quality_tab = QScrollArea()
        scan_quality_tab.setWidgetResizable(True)
        scan_quality_widget = QWidget()
        scan_quality_layout = QVBoxLayout(scan_quality_widget)
        scan_quality_tab.setWidget(scan_quality_widget)

        # Add scan quality content
        self.setup_scan_quality_section(scan_quality_layout)

        # Add tab to tab widget
        self.tabs.addTab(scan_quality_tab, "Scan Details")
        
    def setup_scan_quality_section(self, layout):
        # Scan Indication
        indication_group = QGroupBox("Scan Indication")
        indication_layout = QVBoxLayout()
        
        self.indication_text = QTextEdit()
        self.indication_text.setPlaceholderText("Enter the clinical indication for this scan...")
        self.indication_text.setMaximumHeight(100)
        indication_layout.addWidget(self.indication_text)
        
        indication_group.setLayout(indication_layout)
        layout.addWidget(indication_group)

        # Add spacing between sections
        layout.addSpacing(20)

        # Views Obtained
        views_group = QGroupBox("Views Obtained")
        views_layout = QVBoxLayout()
        
        # Create checkboxes for each view
        self.view_checkboxes = {
            'psax': QCheckBox("Parasternal short axis"),
            'plax': QCheckBox("Parasternal long axis"),
            'a4c': QCheckBox("Apical 4 chamber"),
            'a5c': QCheckBox("Apical 5 chamber"),
            'subx': QCheckBox("Subxiphoid")
        }
        
        # Add checkboxes to layout
        for checkbox in self.view_checkboxes.values():
            views_layout.addWidget(checkbox)
        
        views_group.setLayout(views_layout)
        layout.addWidget(views_group)

        # Add spacing between sections
        layout.addSpacing(20)

        # Scan Quality Assessment
        quality_group = QGroupBox("Scan Quality Assessment")
        quality_layout = QVBoxLayout()

        # Quality options with radio buttons
        quality_button_group = QButtonGroup(self)
        self.quality_buttons = {
            'teaching': QRadioButton("Teaching case - Excellent image quality"),
            'good': QRadioButton("Good - Complete study with good views"),
            'adequate': QRadioButton("Adequate - Key findings visible but some limitations"),
            'poor': QRadioButton("Poor - Significant technical limitations")
        }

        for i, (quality, button) in enumerate(self.quality_buttons.items()):
            quality_layout.addWidget(button)
            quality_button_group.addButton(button)
            if quality == 'adequate':  # Set default selection
                button.setChecked(True)

        # Quality comments section
        quality_layout.addSpacing(10)
        comments_label = QLabel("Quality Comments:")
        quality_layout.addWidget(comments_label)

        self.quality_comments = QLineEdit()
        self.quality_comments.setPlaceholderText("Enter any comments about scan quality...")
        quality_layout.addWidget(self.quality_comments)

        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)

        # Add stretch at the end to push everything to the top
        layout.addStretch()
        
    def create_valve_tab(self):
        valve_tab = QScrollArea()
        valve_tab.setWidgetResizable(True)
        valve_widget = QWidget()
        valve_layout = QVBoxLayout(valve_widget)
        
        self.setup_valve_section(valve_layout)
        
        valve_tab.setWidget(valve_widget)
        self.tabs.addTab(valve_tab, "Valve Assessment")


    def create_patient_info_tab(self):
        patient_info_tab = QScrollArea()
        patient_info_tab.setWidgetResizable(True)
        patient_info_widget = QWidget()
        patient_info_layout = QVBoxLayout(patient_info_widget)
        patient_info_tab.setWidget(patient_info_widget)

        # Add patient info content
        self.setup_patient_info_section(patient_info_layout)

        # Add tab to tab widget
        self.tabs.addTab(patient_info_tab, "Patient Information")

    def setup_patient_info_section(self, layout):
        # Title
        title = QLabel("Patient Information")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        # Create grid layout for patient info
        form_layout = QGridLayout()
        layout.addLayout(form_layout)

        # Note about anonymization
        note_label = QLabel("PLEASE NOTE: ALL REPORTS MUST BE ANONYMISED")
        note_label.setStyleSheet("color: red; font-weight: bold;")
        form_layout.addWidget(note_label, 0, 0, 1, 2)

        # Patient Name
        form_layout.addWidget(QLabel("Patient Name:"), 1, 0)
        self.patient_name = QLineEdit()
        form_layout.addWidget(self.patient_name, 1, 1)

        # MRN/NHS Number
        form_layout.addWidget(QLabel("MRN/NHS No:"), 2, 0)
        self.mrn = QLineEdit()
        form_layout.addWidget(self.mrn, 2, 1)

        # Date of Birth
        form_layout.addWidget(QLabel("Date of Birth:"), 3, 0)
        self.dob = QDateEdit()
        self.dob.setDisplayFormat("dd/MM/yyyy")
        self.dob.setCalendarPopup(True)
        self.dob.setDate(QDate.currentDate())
        form_layout.addWidget(self.dob, 3, 1)

        # Gender
        form_layout.addWidget(QLabel("Gender:"), 4, 0)
        self.gender = QLineEdit()
        form_layout.addWidget(self.gender, 4, 1)

        # Add stretch at the end to push everything to the top
        layout.addStretch()

    def create_ventricular_tab(self):
        ventricular_tab = QScrollArea()
        ventricular_tab.setWidgetResizable(True)
        ventricular_widget = QWidget()
        ventricular_layout = QVBoxLayout(ventricular_widget)
        
        # Setup the ventricular content
        self.setup_ventricular_section(ventricular_layout)
        
        ventricular_tab.setWidget(ventricular_widget)
        self.tabs.addTab(ventricular_tab, "Ventricular Assessment")

    def setup_ventricular_section(self, layout):
        # Left Ventricular Size
        lv_size_group = QGroupBox("Left Ventricular Size")
        lv_size_layout = QVBoxLayout()
        
        self.lv_size_buttons = QButtonGroup(self)
        lv_size_options = [
            ('normal', 'Normal size'),
            ('small', 'Small cavity'),
            ('large', 'Large cavity'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in lv_size_options:
            radio = QRadioButton(text)
            self.lv_size_buttons.addButton(radio)
            lv_size_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        # LVIDD measurement
        lvidd_layout = QHBoxLayout()
        lvidd_label = QLabel("LVIDD (cm):")
        self.lvidd_input = QLineEdit()
        self.lvidd_input.setPlaceholderText("Enter LVIDD value")
        self.lvidd_input.setMaximumWidth(100)
        lvidd_layout.addWidget(lvidd_label)
        lvidd_layout.addWidget(self.lvidd_input)
        lvidd_layout.addStretch()
        lv_size_layout.addLayout(lvidd_layout)
        
        lv_size_group.setLayout(lv_size_layout)
        layout.addWidget(lv_size_group)

        # Left Ventricular Function
        lv_function_group = QGroupBox("Left Ventricular Function")
        lv_function_layout = QVBoxLayout()
        
        self.lv_function_buttons = QButtonGroup(self)
        lv_function_options = [
            ('normal', 'Normal movement'),
            ('impaired', 'Impaired (more than mild)'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in lv_function_options:
            radio = QRadioButton(text)
            self.lv_function_buttons.addButton(radio)
            lv_function_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        # Wall Motion Abnormality Checkbox
        self.wall_motion_check = QCheckBox("Major regional wall motion abnormality")
        lv_function_layout.addWidget(self.wall_motion_check)
        
        lv_function_group.setLayout(lv_function_layout)
        layout.addWidget(lv_function_group)

        # Inter-atrial Septum
        septum_group = QGroupBox("Inter-atrial Septum Shape and Movement")
        septum_layout = QVBoxLayout()
        
        self.septum_buttons = QButtonGroup(self)
        septum_options = [
            ('normal', 'Mid-systolic reversal (normal)'),
            ('right', 'Fixed curvature towards the right atrium'),
            ('left', 'Fixed curvature towards the left atrium'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in septum_options:
            radio = QRadioButton(text)
            self.septum_buttons.addButton(radio)
            septum_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)
        
        septum_group.setLayout(septum_layout)
        layout.addWidget(septum_group)

        # Right Ventricular Size
        rv_size_group = QGroupBox("Right Ventricular Size")
        rv_size_layout = QVBoxLayout()
        
        self.rv_size_buttons = QButtonGroup(self)
        rv_size_options = [
            ('normal', 'Normal'),
            ('small', 'Small cavity'),
            ('enlarged', 'Enlarged'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in rv_size_options:
            radio = QRadioButton(text)
            self.rv_size_buttons.addButton(radio)
            rv_size_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        rv_size_group.setLayout(rv_size_layout)
        layout.addWidget(rv_size_group)

        # Right Ventricular Function
        rv_function_group = QGroupBox("Right Ventricular Function")
        rv_function_layout = QVBoxLayout()
        
        # TAPSE measurement
        tapse_layout = QHBoxLayout()
        tapse_label = QLabel("TAPSE (mm):")
        self.tapse_input = QLineEdit()
        self.tapse_input.setPlaceholderText("Enter TAPSE value")
        self.tapse_input.setMaximumWidth(100)
        tapse_layout.addWidget(tapse_label)
        tapse_layout.addWidget(self.tapse_input)
        tapse_layout.addStretch()
        rv_function_layout.addLayout(tapse_layout)
        
        rv_function_group.setLayout(rv_function_layout)
        layout.addWidget(rv_function_group)

        # Add stretch at the end
        layout.addStretch()
       

        # Add some spacing before valve assessment
        layout.addSpacing(20)

        # Valve Assessment Section
        valve_group = QGroupBox("Valve Assessment")
        valve_layout = QVBoxLayout()

        # Aortic Valve
        av_group = QGroupBox("Aortic Valve Structure & Function")
        av_layout = QVBoxLayout()
        
        self.av_buttons = QButtonGroup(self)
        av_options = [
            ('normal', 'Normal'),
            ('calcified', 'Heavily calcified/restricted opening'),
            ('significant', 'Significant AR/valve prolapse'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in av_options:
            radio = QRadioButton(text)
            self.av_buttons.addButton(radio)
            av_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        av_group.setLayout(av_layout)
        valve_layout.addWidget(av_group)

        # Mitral Valve
        mv_group = QGroupBox("Mitral Valve Structure & Function")
        mv_layout = QVBoxLayout()
        
        self.mv_buttons = QButtonGroup(self)
        mv_options = [
            ('normal', 'Normal'),
            ('calcified', 'Heavily calcified/restricted opening'),
            ('significant', 'Significant MR/valve prolapse'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in mv_options:
            radio = QRadioButton(text)
            self.mv_buttons.addButton(radio)
            mv_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        mv_group.setLayout(mv_layout)
        valve_layout.addWidget(mv_group)

        # Tricuspid Valve
        tv_group = QGroupBox("Tricuspid Valve Structure & Function")
        tv_layout = QVBoxLayout()
        
        self.tv_buttons = QButtonGroup(self)
        tv_options = [
            ('normal', 'Normal'),
            ('calcified', 'Heavily calcified/restricted opening'),
            ('significant', 'Significant TR/valve prolapse'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in tv_options:
            radio = QRadioButton(text)
            self.tv_buttons.addButton(radio)
            tv_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        tv_group.setLayout(tv_layout)
        valve_layout.addWidget(tv_group)

        valve_group.setLayout(valve_layout)
        layout.addWidget(valve_group)

        # Add stretch at the end
        layout.addStretch()
        
    def setup_valve_section(self, layout):
        # Aortic Valve
        av_group = QGroupBox("Aortic Valve Structure & Function")
        av_layout = QVBoxLayout()
        
        self.av_buttons = QButtonGroup(self)
        av_options = [
            ('normal', 'Normal'),
            ('calcified', 'Heavily calcified/restricted opening'),
            ('significant', 'Significant AR/valve prolapse'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in av_options:
            radio = QRadioButton(text)
            self.av_buttons.addButton(radio)
            av_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        av_group.setLayout(av_layout)
        layout.addWidget(av_group)

        # Mitral Valve
        mv_group = QGroupBox("Mitral Valve Structure & Function")
        mv_layout = QVBoxLayout()
        
        self.mv_buttons = QButtonGroup(self)
        mv_options = [
            ('normal', 'Normal'),
            ('calcified', 'Heavily calcified/restricted opening'),
            ('significant', 'Significant MR/valve prolapse'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in mv_options:
            radio = QRadioButton(text)
            self.mv_buttons.addButton(radio)
            mv_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        mv_group.setLayout(mv_layout)
        layout.addWidget(mv_group)

        # Tricuspid Valve
        tv_group = QGroupBox("Tricuspid Valve Structure & Function")
        tv_layout = QVBoxLayout()
        
        self.tv_buttons = QButtonGroup(self)
        tv_options = [
            ('normal', 'Normal'),
            ('calcified', 'Heavily calcified/restricted opening'),
            ('significant', 'Significant TR/valve prolapse'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in tv_options:
            radio = QRadioButton(text)
            self.tv_buttons.addButton(radio)
            tv_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        tv_group.setLayout(tv_layout)
        layout.addWidget(tv_group)

        # Add stretch at the end
        layout.addStretch()

    def create_other_findings_tab(self):
        other_findings_tab = QScrollArea()
        other_findings_tab.setWidgetResizable(True)
        other_findings_widget = QWidget()
        other_findings_layout = QVBoxLayout(other_findings_widget)
        
        self.setup_other_findings_section(other_findings_layout)
        
        other_findings_tab.setWidget(other_findings_widget)
        self.tabs.addTab(other_findings_tab, "Other Findings")

    def setup_other_findings_section(self, layout):
        # Aortic Root
        aortic_root_group = QGroupBox("Aortic Root")
        aortic_root_layout = QVBoxLayout()
        
        self.aortic_root_buttons = QButtonGroup(self)
        aortic_root_options = [
            ('normal', 'Visually normal size'),
            ('dilated', 'Dilated'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in aortic_root_options:
            radio = QRadioButton(text)
            self.aortic_root_buttons.addButton(radio)
            aortic_root_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        aortic_root_group.setLayout(aortic_root_layout)
        layout.addWidget(aortic_root_group)

        # Add spacing between sections
        layout.addSpacing(20)

        # IVC
        ivc_group = QGroupBox("IVC")
        ivc_layout = QVBoxLayout()
        
        self.ivc_buttons = QButtonGroup(self)
        ivc_options = [
            ('small', 'Small and/or collapsing'),
            ('normal', 'Normal movement with respiration'),
            ('large', 'Large and/or non-collapsing'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in ivc_options:
            radio = QRadioButton(text)
            self.ivc_buttons.addButton(radio)
            ivc_layout.addWidget(radio)
            if value == 'normal':
                radio.setChecked(True)

        ivc_group.setLayout(ivc_layout)
        layout.addWidget(ivc_group)

        # Add spacing
        layout.addSpacing(20)

        # Pericardial Fluid
        pericardial_group = QGroupBox("Pericardial Fluid")
        pericardial_layout = QVBoxLayout()
        
        self.pericardial_buttons = QButtonGroup(self)
        pericardial_options = [
            ('none', 'No pericardial fluid seen'),
            ('trivial', 'Trivial'),
            ('significant', 'Significant, +/- signs of tamponade'),
            ('unable', 'Unable to assess')
        ]
        
        for value, text in pericardial_options:
            radio = QRadioButton(text)
            self.pericardial_buttons.addButton(radio)
            pericardial_layout.addWidget(radio)
            if value == 'none':
                radio.setChecked(True)

        pericardial_group.setLayout(pericardial_layout)
        layout.addWidget(pericardial_group)

        # Add spacing
        layout.addSpacing(20)

        # Pleural Effusion
        pleural_group = QGroupBox("Pleural Effusion")
        pleural_layout = QVBoxLayout()
        
        
        # Pleural Effusion
        # Use checkbox for yes/no
        pleural_group = QGroupBox("Pleural Effusion")
        pleural_layout = QVBoxLayout()
        
        self.pleural_buttons = QButtonGroup(self)
        pleural_options = [
            ('yes', 'Present'),
            ('no', 'Not Present')
        ]
        
        for value, text in pleural_options:
            radio = QRadioButton(text)
            self.pleural_buttons.addButton(radio)
            pleural_layout.addWidget(radio)
            if value == 'no':  # Default to Not Present
                radio.setChecked(True)
        
        pleural_group.setLayout(pleural_layout)
        layout.addWidget(pleural_group)

        # Add spacing
        layout.addSpacing(20)

        # Additional Observations
        observations_group = QGroupBox("Additional Observations")
        observations_layout = QVBoxLayout()
        
        self.observations_text = QLineEdit()
        self.observations_text.setPlaceholderText("Enter any additional observations...")
        observations_layout.addWidget(self.observations_text)
        
        observations_group.setLayout(observations_layout)
        layout.addWidget(observations_group)

        # Add stretch at the end
        layout.addStretch()
    
    def create_conclusions_tab(self):
        conclusions_tab = QScrollArea()
        conclusions_tab.setWidgetResizable(True)
        conclusions_widget = QWidget()
        conclusions_layout = QVBoxLayout(conclusions_widget)
        
        self.setup_conclusions_section(conclusions_layout)
        
        conclusions_tab.setWidget(conclusions_widget)
        self.tabs.addTab(conclusions_tab, "Conclusions")

    def setup_conclusions_section(self, layout):
        # Clinical Conclusion
        conclusion_group = QGroupBox("Clinical Conclusion")
        conclusion_layout = QVBoxLayout()
        
        note_label = QLabel("(referenced to the clinical question)")
        note_label.setStyleSheet("font-style: italic;")
        conclusion_layout.addWidget(note_label)

        self.conclusions_text = QTextEdit()
        self.conclusions_text.setMinimumHeight(200)
        self.conclusions_text.setPlaceholderText("Enter your clinical conclusion here...")
        conclusion_layout.addWidget(self.conclusions_text)
        
        conclusion_group.setLayout(conclusion_layout)
        layout.addWidget(conclusion_group)

        # Add separator
        layout.addSpacing(20)

        # Training Approval Section
        training_group = QGroupBox("Training Scan Approval")
        training_layout = QVBoxLayout()

        # Approval input
        approval_layout = QHBoxLayout()
        approval_label = QLabel("Report checked and approved by:")
        self.approval_input = QLineEdit()
        approval_layout.addWidget(approval_label)
        approval_layout.addWidget(self.approval_input)
        training_layout.addWidget(QWidget())  # Spacing
        training_layout.addLayout(approval_layout)

        # Warning note
        warning_label = QLabel("(training reports are not to be used for patient care unless checked and approved)")
        warning_label.setStyleSheet("font-style: italic; color: red;")
        training_layout.addWidget(warning_label)

        training_group.setLayout(training_layout)
        layout.addWidget(training_group)

        # Add separator
        layout.addSpacing(20)

        # Level 2 Study Section
        level2_group = QGroupBox("Level 2 Study Requirement")
        level2_layout = QVBoxLayout()
        
        self.level2_buttons = QButtonGroup(self)
        level2_options = [
            ('yes', 'Yes'),
            ('no', 'No')
        ]
        
        level2_label = QLabel("Does the patient need a Level 2 study?")
        level2_layout.addWidget(level2_label)
        
        for value, text in level2_options:
            radio = QRadioButton(text)
            self.level2_buttons.addButton(radio)
            level2_layout.addWidget(radio)
            if value == 'no':
                radio.setChecked(True)

        level2_group.setLayout(level2_layout)
        layout.addWidget(level2_group)

        # Add separator
        layout.addSpacing(20)

        # Referring Physician Section
        physician_group = QGroupBox("Referring Physician")
        physician_layout = QVBoxLayout()
        
        self.physician_buttons = QButtonGroup(self)
        physician_options = [
            ('yes', 'Yes'),
            ('no', 'No')
        ]
        
        physician_label = QLabel("Referring physician informed?")
        physician_layout.addWidget(physician_label)
        
        for value, text in physician_options:
            radio = QRadioButton(text)
            self.physician_buttons.addButton(radio)
            physician_layout.addWidget(radio)
            if value == 'no':
                radio.setChecked(True)

        physician_group.setLayout(physician_layout)
        layout.addWidget(physician_group)

        # Add separator
        layout.addSpacing(20)

        # Name and Training Status
        status_group = QGroupBox("Reporter Details")
        status_layout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        status_layout.addLayout(name_layout)
        
        training_layout = QHBoxLayout()
        training_label = QLabel("Training Status:")
        self.training_status_input = QLineEdit()
        training_layout.addWidget(training_label)
        training_layout.addWidget(self.training_status_input)
        status_layout.addLayout(training_layout)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        # Add stretch at the end
        layout.addStretch()
    
    
    def save_report(self):
        # Format data for database (flatten the nested dictionaries)
        report_data = {
            # Patient Info
            'patient_name': self.patient_name.text(),
            'mrn': self.mrn.text(),
            'dob': self.dob.date().toString("dd/MM/yyyy"),
            'gender': self.gender.text(),
            
            # Scan Quality & Views
            'scan_indication': self.indication_text.toPlainText(),
            'scan_quality': next(quality for quality, button in self.quality_buttons.items() 
                               if button.isChecked()),
            'quality_comments': self.quality_comments.text(),
            'view_psax': self.view_checkboxes['psax'].isChecked(),
            'view_plax': self.view_checkboxes['plax'].isChecked(),
            'view_a4c': self.view_checkboxes['a4c'].isChecked(),
            'view_a5c': self.view_checkboxes['a5c'].isChecked(),
            'view_subx': self.view_checkboxes['subx'].isChecked(),
            
            # Ventricular Assessment
            'lv_size': next(button.text() for button in self.lv_size_buttons.buttons() 
                          if button.isChecked()),
            'lvidd': self.lvidd_input.text(),
            'lv_function': next(button.text() for button in self.lv_function_buttons.buttons() 
                              if button.isChecked()),
            'wall_motion_abnormality': self.wall_motion_check.isChecked(),
            'rv_size': next(button.text() for button in self.rv_size_buttons.buttons() 
                          if button.isChecked()),
            'tapse': self.tapse_input.text(),
            
            # Septum
            'septum_shape': next(button.text() for button in self.septum_buttons.buttons() 
                               if button.isChecked()),
            
            # Valve Assessment
            'av_status': next(button.text() for button in self.av_buttons.buttons() 
                            if button.isChecked()),
            'mv_status': next(button.text() for button in self.mv_buttons.buttons() 
                            if button.isChecked()),
            'tv_status': next(button.text() for button in self.tv_buttons.buttons() 
                            if button.isChecked()),
            
            # Other Findings
            'aortic_root': next(button.text() for button in self.aortic_root_buttons.buttons() 
                               if button.isChecked()),
            'ivc': next(button.text() for button in self.ivc_buttons.buttons() 
                       if button.isChecked()),
            'pericardial_fluid': next(button.text() for button in self.pericardial_buttons.buttons() 
                                    if button.isChecked()),
            'pleural_effusion': next(button.text() for button in self.pleural_buttons.buttons() 
                                   if button.isChecked()),
            'additional_observations': self.observations_text.text(),
            
            # Conclusions
            'clinical_conclusion': self.conclusions_text.toPlainText(),
            'training_approval': self.approval_input.text(),
            'requires_level2': next(button.text() for button in self.level2_buttons.buttons() 
                                  if button.isChecked()) == 'Yes',
            'physician_informed': next(button.text() for button in self.physician_buttons.buttons() 
                                    if button.isChecked()) == 'Yes',
            'reporter_name': self.name_input.text(),
            'training_status': self.training_status_input.text()
        }
        
        try:
            # Save to database
            report_id = self.db.save_report(report_data)
            print(f"\nReport saved to database with ID: {report_id}")
            
            # Print data for verification
            print("\nSaved Data:")
            for key, value in report_data.items():
                print(f"{key}: {value}")
                
        except Exception as e:
            print(f"Error saving report: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = EchoReportApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()