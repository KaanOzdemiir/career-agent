from typing import List, Optional

from pydantic import BaseModel, Field


class Personal(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None


class Experience(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    achievements: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)


class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Language(BaseModel):
    language: Optional[str] = None
    proficiency: Optional[str] = None


class Candidate(BaseModel):
    personal: Personal
    headline: Optional[str] = None
    summary: Optional[str] = None

    current_title: Optional[str] = None
    current_company: Optional[str] = None
    total_years_experience: Optional[float] = None

    primary_role_family: Optional[str] = None
    companies: List[str] = Field(default_factory=list)
    previous_titles: List[str] = Field(default_factory=list)

    programming_languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    industries: List[str] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[Language] = Field(default_factory=list)


class CareerProfile(BaseModel):
    preferred_roles: List[str] = Field(default_factory=list)
    preferred_countries: List[str] = Field(default_factory=list)
    remote: bool = True
    hybrid: bool = True
    onsite: bool = False
    minimum_salary_eur: Optional[int] = None