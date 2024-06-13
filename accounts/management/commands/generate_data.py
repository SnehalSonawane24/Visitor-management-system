from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.factories import UserAccountFactory
from organisation.factories import (
    OrganisationFactory,
    UnitFactory,
    GateFactory,
    DepartmentFactory,
    EmployeeProfileFactory,
    EmployeeAuthorizationFactory,
)
from visitor.factories import VisitorProfileFactory, VisitFactory

from faker import Faker

import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

fake = Faker()


class Command(BaseCommand):
    help = "Generates fixtures using factories for all apps"

    def handle(self, *args, **options):
        user_records = 2
        organisation_records_per_user = 2
        unit_records_per_org = 2
        gate_records_per_unit = 2
        department_records_per_org = 2
        employee_records_per_department = 2
        visitor_profile_records_per_employee = 2
        visit_records_per_visitor = 50

        with transaction.atomic():
            # Generate fixtures for UserAccount
            users = UserAccountFactory.create_batch(user_records)

            for user in users:
                # Generate fixtures for Organisation
                organisations = OrganisationFactory.create_batch(
                    organisation_records_per_user, created_by=user, updated_by=user
                )

                for organisation in organisations:
                    # Generate fixtures for Unit
                    units = UnitFactory.create_batch(
                        unit_records_per_org,
                        org=organisation,
                        created_by=user,
                        updated_by=user,
                    )

                    for unit in units:
                        # Generate fixtures for Gate
                        gates = GateFactory.create_batch(
                            gate_records_per_unit,
                            unit=unit,
                            created_by=user,
                            updated_by=user,
                        )

                    # Generate fixtures for Department
                    departments = DepartmentFactory.create_batch(
                        department_records_per_org,
                        org=organisation,
                        created_by=user,
                        updated_by=user,
                    )

                    for department in departments:
                        # Generate fixtures for EmployeeProfile
                        employees = EmployeeProfileFactory.create_batch(
                            employee_records_per_department,
                            department=department,
                            created_by=user,
                            updated_by=user,
                        )

                        for employee in employees:
                            # Generate fixtures for EmployeeAuthorization
                            EmployeeAuthorizationFactory.create(
                                employee=employee,
                                user_acc=user,
                                created_by=user,
                                updated_by=user,
                            )

                            # Generate fixtures for VisitorProfile
                            visitors = VisitorProfileFactory.create_batch(
                                visitor_profile_records_per_employee,
                                created_by=user,
                                updated_by=user,
                            )

                            for visitor in visitors:
                                # Generate fixtures for Visit
                                visits = VisitFactory.create_batch(
                                    visit_records_per_visitor,
                                    visitor=visitor,
                                    employee=employee,
                                    gate=gates[0],
                                    created_by=user,
                                    updated_by=user,
                                )

                                # Modify visits for different timeframes
                                VisitFactory.create(
                                    visitor=visitor,
                                    employee=employee,
                                    gate=gates[0],
                                    check_in=fake.date_time_between(
                                        start_date="-1d", end_date="now"
                                    ),
                                    check_out=None,
                                    created_by=user,
                                    updated_by=user,
                                )

            logger.info(
                f"{user_records} records generated successfully for UserAccount."
            )
            logger.info(
                f"{user_records * organisation_records_per_user} records generated successfully for Organisation."
            )
            logger.info(
                f"{user_records * organisation_records_per_user * unit_records_per_org} records generated successfully for Unit."
            )
            logger.info(
                f"{user_records * organisation_records_per_user * unit_records_per_org * gate_records_per_unit} records generated successfully for Gate."
            )
            logger.info(
                f"{user_records * organisation_records_per_user * department_records_per_org} records generated successfully for Department."
            )
            logger.info(
                f"{user_records * organisation_records_per_user * department_records_per_org * employee_records_per_department} records generated successfully for EmployeeProfile."
            )
            logger.info(
                f"{user_records * organisation_records_per_user * department_records_per_org * employee_records_per_department * visitor_profile_records_per_employee} records generated successfully for VisitorProfile."
            )
            logger.info(
                f"{user_records * organisation_records_per_user * department_records_per_org * employee_records_per_department * visitor_profile_records_per_employee * visit_records_per_visitor} records generated successfully for Visit."
            )
