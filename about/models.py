# ABOUT · MODELOS ADMINISTRATIVOS INDEPENDIENTES | ABOUT · INDEPENDENT ADMIN MODELS
# Etapa 1: proxies que utilizan las tablas actuales; no duplican ni mueven registros.
from core.models import AboutContent as LegacyAboutContent
from core.visual_config import AboutPageConfiguration as LegacyAboutPageConfiguration


class AboutContent(LegacyAboutContent):
    class Meta:
        proxy = True
        verbose_name = "001 - About Us"
        verbose_name_plural = "001 - About Us"


class AboutPageConfiguration(LegacyAboutPageConfiguration):
    class Meta:
        proxy = True
        verbose_name = "002 - About Visual Configuration"
        verbose_name_plural = "002 - About Visual Configuration"

# ABOUT · CONTENIDO CORPORATIVO | ABOUT · COMPANY CONTENT
# Solo proxies: todos reutilizan las tablas y los archivos de core.
from core.models import (
    TeamMember as LegacyTeamMember,
    Insurance as LegacyInsurance,
    Certification as LegacyCertification,
    CompanyValue as LegacyCompanyValue,
    ProcessStep as LegacyProcessStep,
)

class TeamMember(LegacyTeamMember):
    class Meta:
        proxy = True
        verbose_name = "003 - Team"
        verbose_name_plural = "003 - Team"

class Insurance(LegacyInsurance):
    class Meta:
        proxy = True
        verbose_name = "004 - Insurance"
        verbose_name_plural = "004 - Insurance"

class Certification(LegacyCertification):
    class Meta:
        proxy = True
        verbose_name = "005 - Certifications"
        verbose_name_plural = "005 - Certifications"

class CompanyValue(LegacyCompanyValue):
    class Meta:
        proxy = True
        verbose_name = "006 - Company Value"
        verbose_name_plural = "006 - Company Values"

class ProcessStep(LegacyProcessStep):
    class Meta:
        proxy = True
        verbose_name = "007 - Work Process"
        verbose_name_plural = "007 - Work Process"
