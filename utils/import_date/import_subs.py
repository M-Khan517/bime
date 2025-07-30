import pandas as pd
from apps.account_module.models import User, SubUser


def import_subs_for_manager(manager, excel_file):
    df = pd.read_excel(excel_file, dtype={"national_code": str})
    subs = []
    errors = []
    results = {}
    for _, row in df.iterrows():
        if (
            str(row.get("full_name", "")) is None
            or str(row.get("full_name", "")) == ""
            or str(row.get("national_code", "")) is None
            or str(row.get("national_code", "")) == ""
        ):
            errors.append("خطا در خواندن اطلاعات")
            continue
        sub_name = str(row.get("full_name", "")).strip()
        national_code = str(row.get("national_code", "")).strip()

        check_sub_is_exists = SubUser.objects.filter(
            national_code=national_code
        ).exists()

        if check_sub_is_exists == False:
            if len(national_code) == 10 or len(national_code) == 13:
                subs.append(
                    SubUser(
                        full_name=sub_name, national_code=national_code, manager=manager
                    )
                )
            else:
                errors.append(f"کدملی {national_code} معتبر نمی باشد")
        else:
            errors.append(f"کد ملی {national_code} قبلا ثبت شده است")

    if len(subs) > 0:
        SubUser.objects.bulk_create(subs)
        results["success_add"] = len(subs)

    print("import done ...")

    results["errors"] = errors

    return results
