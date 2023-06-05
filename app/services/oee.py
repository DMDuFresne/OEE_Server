from app.models.oee import OeeModel


def calculate_oee(data):
    oee_model = OeeModel(**data)

    availability = oee_model.run_time / oee_model.planned_production_time
    performance = (oee_model.total_count / oee_model.run_time) / oee_model.ideal_run_rate
    quality = oee_model.good_count / oee_model.total_count

    oee = availability * performance * quality

    return {"oee": oee}
