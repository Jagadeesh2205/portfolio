export interface Experience {
  id: string;
  period: string;
  company: string;
  role: string;
  startMonth: string;
  endMonth: string;
  ongoing: boolean;
  bullets: string[];
}

export const experienceData: Experience[] = [
  {
    id: "1",
    period: "2026",
    company: "Ethara AI",
    role: "Data Annotation & LLM Evaluator",
    startMonth: "Mar 2026",
    endMonth: "May 2026",
    ongoing: false,
    bullets: [
      "Performed structured data annotation for LLM training pipelines.",
      "Conducted post-training LLM response evaluation — assessing quality, accuracy, and instruction-following across model outputs."
    ]
  },
  {
    id: "2",
    period: "2024-2025",
    company: "Infosys Springboard",
    role: "AI & ML Intern",
    startMonth: "Nov 2024",
    endMonth: "Jan 2025",
    ongoing: false,
    bullets: [
      "Designed and trained a multi-class CNN classifier for Advanced Skin Disease Diagnosis, achieving 94% test accuracy and 0.91 Macro-F1 across 9 disease categories on 27,000 images.",
      "Applied MLOps principles including experiment tracking, model versioning, and Docker containerization to ensure full reproducibility.",
      "Served model predictions via a high-performance Flask REST API."
    ]
  },
  {
    id: "3",
    period: "2023-2024",
    company: "Teachnook",
    role: "ML Intern",
    startMonth: "2023",
    endMonth: "2024",
    ongoing: false,
    bullets: [
      "Implemented core ML algorithms from scratch and with Scikit-learn: regression, classification, clustering.",
      "Applied algorithms to real datasets for hands-on understanding of model selection and evaluation."
    ]
  }
];
