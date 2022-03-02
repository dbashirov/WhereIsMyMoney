from django.contrib.admin.apps import AdminConfig


class FinanceAdminConfig(AdminConfig):
    default_site = 'finance_project.admin.FinanceAdmin'