from .exports.rows.user_export_row import UserExportRow
from .exports.rows.car_export_row import CarExportRow
from .exports.rows.commit_export_row import CommitExportRow
from .exports.rows.trip_export_row import TripExportRow
from .exports.rows.refueling_export_row import RefuelingExportRow
from ...logger import get_logger


class ExportService:
    def __init__(
        self,
        user_repository,
        car_repository,
        trip_repository,
        commit_repository,
        refueling_repository,
        excel_writer,
    ):
        self.user_repository = user_repository
        self.car_repository = car_repository
        self.trip_repository = trip_repository
        self.commit_repository = commit_repository
        self.refueling_repository = refueling_repository
        self.excel_writer = excel_writer
        self.logger = get_logger(__name__)

    def export_data(self) -> bytes:
        refuelings = self.refueling_repository.find_all()
        cars = self.car_repository.find_all()
        commits = self.commit_repository.find_all()
        trips = self.trip_repository.find_all()
        users = self.user_repository.find_all()

        users_by_id = {
            user.id: user
            for user in users
        }

        cars_by_id = {
            car.id: car
            for car in cars
        }

        commits_by_trip_id: dict[str, list] = {}

        for commit in commits:
            commits_by_trip_id.setdefault(
                commit.trip_id,
                []
            ).append(commit)

        user_rows = [
            UserExportRow(
                name=user.name,
                email=user.email,
                role=user.role.value,
            )
            for user in users
        ]

        car_rows = [
            CarExportRow(
                plate=car.plate,
                model=car.model,
                km_total=car.mileage.km_total,
                km_servicing=car.mileage.km_servicing,
                km_wheels=car.mileage.km_wheels,
                fuel_type=car.fuel_info.type,
                fuel_level=car.fuel_info.level,
                fuel_card=car.fuel_info.card,
                co2_per_km=car.co2_per_km,
            )
            for car in cars
        ]

        self.logger.debug(f"Exporting {len(users)} users, {len(cars)} cars, {len(commits)} commits, {len(trips)} trips, and {len(refuelings)} refuelings.")
        self.logger.debug(f"Car export rows: {car_rows}")

        commit_rows = [
            CommitExportRow(
                code=commit.code,
                description=commit.description,
            )
            for commit in commits
        ]

        trip_rows = []

        for trip in trips:
            user = users_by_id.get(trip.user_id)
            car = cars_by_id.get(trip.car_id)

            trip_commits = commits_by_trip_id.get(
                trip.id,
                []
            )

            commit_codes = ", ".join(
                commit.code
                for commit in trip_commits
            )
            start_date = trip.start_date.replace(tzinfo=None)
            end_date = trip.end_date.replace(tzinfo=None) if trip.end_date else None
            trip_rows.append(
                TripExportRow(
                    user_email=user.email if user else "",
                    car_plate=car.plate if car else "",
                    commits=commit_codes,
                    start_position=trip.start_position,
                    end_position=trip.end_position,
                    start_date=start_date,
                    end_date=end_date,
                    start_km=trip.start_km,
                    end_km=trip.end_km,
                    distance=trip.distance,
                    duration_minutes=trip.duration,
                    status=trip.status.value,
                )
            )

        refueling_rows = []

        for refueling in refuelings:
            car = cars_by_id.get(refueling.car_id)

            refueling_rows.append(
                RefuelingExportRow(
                    car_plate=car.plate if car else "",
                    card_number=refueling.card_number,
                    liter_price=refueling.liter_price,
                    liters=refueling.liters,
                    total_price=refueling.liter_price * refueling.liters,
                    date=refueling.date.replace(tzinfo=None),
                    receipt_photo=refueling.receipt_photo,
                )
            )

        return self.excel_writer.write(
            users=user_rows,
            cars=car_rows,
            commits=commit_rows,
            trips=trip_rows,
            refuelings=refueling_rows,
        )