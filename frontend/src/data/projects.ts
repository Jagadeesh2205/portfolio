export interface Project {
  id: string;
  category: string;
  title: string;
  thumbnail: string;
  fallbackThumbnail?: string;
  description: string;
  technologies: string[];
  links: { label: string; url: string }[];
  screenshots: string[];
  fallbackScreenshots?: string[];
}

const githubProfile = "https://github.com/Jagadeesh2205";

export const projectsData: Project[] = [
  {
    id: "1",
    category: "Hybrid Graph-RAG & Multi-Agent AI",
    title: "Plant Brain — AI Platform for Industrial Knowledge Intelligence",
    thumbnail: "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?q=80&w=900&auto=format&fit=crop",
    description: "Converts complex industrial manuals and logs into a queryable knowledge system using Hybrid Graph-RAG (ChromaDB + NetworkX) and 3 specialized AI agents (Expert Copilot, Maintenance RCA, Compliance Analyzer). Reduces retrieval time from 23 mins to 3 seconds.",
    technologies: ["React 18", "TypeScript", "FastAPI", "ChromaDB", "NetworkX", "spaCy NER", "ONNX Runtime", "Azure AI Foundry", "Docker"],
    links: [
      { label: "GitHub Repository", url: `${githubProfile}/AI-for-Industrial-Knowledge-Intelligence-Unified-Asset` }
    ],
    screenshots: []
  },
  {
    id: "2",
    category: "Computer Vision & Medical AI",
    title: "Diabetic Retinopathy Detection using Deep Learning",
    thumbnail: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?q=80&w=900&auto=format&fit=crop",
    description: "Automates 5-grade diabetic retinopathy grading using MobileNetV3Small with CBAM (Convolutional Block Attention Module) custom spatial and channel attention layers. Achieved 89% accuracy on APTOS 2019 and 83% cross-dataset generalization on 50,000+ EyePACS images.",
    technologies: ["TensorFlow", "Keras", "OpenCV", "CBAM Attention", "MobileNetV3", "Albumentations", "Python"],
    links: [
      { label: "GitHub Profile", url: githubProfile }
    ],
    screenshots: []
  },
  {
    id: "3",
    category: "MLOps & Dermoscopy AI",
    title: "Skin Disease Classification — Infosys Springboard Internship",
    thumbnail: "https://images.unsplash.com/photo-1576091160550-2173dba999ef?q=80&w=900&auto=format&fit=crop",
    description: "Multi-class CNN classifier trained across 27,000 dermoscopy images for advanced skin condition diagnosis. Containerized with Docker and served via Flask REST API with a Macro-F1 score of 0.91 across imbalanced disease categories.",
    technologies: ["TensorFlow", "Flask", "Docker", "REST API", "Python", "MLOps"],
    links: [
      { label: "GitHub Repository", url: `${githubProfile}/Advance-Skin-disease-diagnosis-using-Image-processing` }
    ],
    screenshots: []
  },
  {
    id: "4",
    category: "Automation & Messaging API",
    title: "WhatsApp Appointment Booking System",
    thumbnail: "https://images.unsplash.com/photo-1611746872915-64382b5c76da?q=80&w=900&auto=format&fit=crop",
    description: "Stateless webhook-driven clinic appointment scheduling platform built with Node.js and Twilio WhatsApp Business API, saving bookings directly into Supabase PostgreSQL.",
    technologies: ["Node.js", "Twilio API", "Supabase", "PostgreSQL", "Vercel", "REST APIs"],
    links: [
      { label: "GitHub Profile", url: githubProfile }
    ],
    screenshots: []
  }
];
