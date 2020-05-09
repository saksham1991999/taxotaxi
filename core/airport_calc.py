from . import models
import datetime
def airport_calculator(pickup_city, drop_city, distance, duration, pickup_datetime):
    print(pickup_city, drop_city)
    print('------------------ Distance ------------------------------------')
    print(distance)
    print('------------------ Duration ------------------------------------')
    print(duration)
    print('------------------ Pickup Date Time ------------------------------------')
    print(pickup_datetime)
    car_types = models.car_types.objects.all()

    car_types_price = []
    car_types_price_km = []
    car_types_allowances = []
    car_types_additional_charges = []
    car_types_early_pickup_charges = []
    car_types_late_drop_charges = []
    car_types_night_charges = []
    car_types_gst_charges = []

    # DROP TIME CALCULATION
    timedelta = datetime.timedelta(minutes=duration)
    drop_datetime = pickup_datetime + timedelta
    print('------------------ Actual Drop Time ------------------------------------')
    print(drop_datetime)
    journey_hour = duration / 60

    hault_time_qs = models.expected_time_hault.objects.all()
    max_hault_time = 0
    for hault_time in hault_time_qs:
        if journey_hour > hault_time.ride_time:
            max_hault_time = max(max_hault_time, hault_time.hault_time)
    print('------------------ Hault Time ------------------------------------')
    print(max_hault_time)
    drop_datetime = drop_datetime + datetime.timedelta(minutes=max_hault_time)
    print('------------------ Expected Drop Time ------------------------------------')
    print(drop_datetime)

    for type in car_types:
        mul_price = distance
        add_price = 0
        print('------------------ Car Type ------------------------------------')
        print(type)
        attrs = models.calc_city_attr_value.objects.filter(city1=pickup_city, city2=drop_city, car_type=type)
        price_km_attr = models.calc_attr.objects.get(name='price_km')
        car_types_price_km.append(attrs.get(attr=price_km_attr).value)
        print('------------------ Price Per Km ------------------------------------')
        print(price_km_attr.value)

        active_mul_attr = models.calc_attr.objects.filter(active=True, is_multiplied=True, is_time_dependent=False)
        for attr in active_mul_attr:
            value = attrs.get(attr=attr).value
            mul_price *= value
        print('------------------ Price After Multiplied Values ------------------------------------')
        print(mul_price)
        car_types_allowances.append(int(mul_price))

        lmb_charge_attrs = models.calc_attr.objects.filter(active=True, is_multiplied=True, is_time_dependent=True, name__startswith='lmb')
        max_lmb_charge = 1
        for lmb_charge_attr in lmb_charge_attrs:
            name = lmb_charge_attr.name
            time = int(name[3:5])
            lmb_timedelta = datetime.timedelta(minutes=time*60)
            lmb_timediff = pickup_datetime - datetime.datetime.now()
            if lmb_timediff < lmb_timedelta:
                max_lmb_charge = max(max_lmb_charge,lmb_charge_attr.value)
        mul_price = mul_price*max_lmb_charge

        print('------------------ Price After LMB Values ------------------------------------')
        print(mul_price)

        active_add_nontime = models.calc_attr.objects.filter(active=True, is_multiplied=False, is_time_dependent=False)
        for attr in active_add_nontime:
            value = attrs.get(attr=attr).value
            add_price += value
        print('------------------ Additional Charges ------------------------------------')
        print(add_price)
        car_types_additional_charges.append(int(add_price))


        time_dependent = models.calc_attr.objects.filter(active=True, is_time_dependent=True)
        night_charge, late_drop_charge, early_pickup_charge = 0, 0, 0

        early_pickup_charge_attrs = time_dependent.filter(name__startswith='epc')
        for early_pickup_charge_attr in early_pickup_charge_attrs:
            name = early_pickup_charge_attr.name
            start_time = int(name[3:5])
            end_time = int(name[6:])
            if end_time > start_time:
                if start_time <= pickup_datetime.hour < end_time:
                    early_pickup_charge = max(early_pickup_charge, early_pickup_charge_attr.value)
            else:
                if start_time <= pickup_datetime.hour <= 24 or 0 <= pickup_datetime.hour <= end_time:
                    early_pickup_charge = max(early_pickup_charge, early_pickup_charge_attr.value)
        print('------------------ Early Pickup Charges ------------------------------------')
        print(early_pickup_charge)
        car_types_early_pickup_charges.append(int(early_pickup_charge))

        late_drop_charge_attrs = time_dependent.filter(name__startswith='ldc')
        for late_drop_charge_attr in late_drop_charge_attrs:
            name = late_drop_charge_attr.name
            start_time = int(name[3:5])
            end_time = int(name[6:])
            if end_time > start_time:
                if start_time <= drop_datetime.hour < end_time:
                    late_drop_charge = max(late_drop_charge, late_drop_charge_attr.value)
            else:
                if start_time <= drop_datetime.hour <= 24 or 0 <= drop_datetime.hour <= end_time:
                    late_drop_charge = max(late_drop_charge, late_drop_charge_attr.value)
        print('------------------ Late Drop Charges ------------------------------------')
        print(late_drop_charge)
        car_types_late_drop_charges.append(int(late_drop_charge))

        journey_days = drop_datetime.date() - pickup_datetime.date()
        journey_days = journey_days.days
        night_charge_attrs_value = time_dependent.filter(name__startswith='nc')[0].value
        if journey_days > 1:
            night_charge = journey_days*night_charge_attrs_value
        else:
            night_charge_attrs = time_dependent.filter(name__startswith='nc')
            for night_charge_attr in night_charge_attrs:
                name = night_charge_attr.name
                start_time = int(name[2:4])
                end_time = int(name[5:])
                if end_time > start_time:
                    if start_time <= pickup_datetime.hour < end_time or start_time <= drop_datetime.hour < end_time:
                        night_charge = max(night_charge, night_charge_attr.value)
                else:
                    if start_time <= pickup_datetime.hour <= 24 or 0 <= pickup_datetime.hour <= end_time or start_time <= drop_datetime.hour <= 24 or 0 <= drop_datetime.hour <= end_time:
                        night_charge = max(night_charge, night_charge_attr.value)
        print('------------------ Night Charges ------------------------------------')
        print(night_charge)
        car_types_night_charges.append(int(night_charge))

        final_price = mul_price + add_price + early_pickup_charge + late_drop_charge + night_charge
        print('------------------ Final Ride Charges Before GST ------------------------------------')
        print(final_price)

        #_______________________GST________________________________
        gst_attr = models.calc_attr.objects.filter(name__exact='gst')[0]
        gst_charges = 0
        if gst_attr.active:
            gst_value = attrs.get(attr = gst_attr).value
            gst_charges = final_price*(gst_value-1)
            car_types_gst_charges.append(int(gst_charges))

        final_price = gst_charges + final_price

        car_types_price.append(int(final_price))
    return car_types_price, car_types_price_km, drop_datetime, car_types_allowances, car_types_additional_charges, car_types_early_pickup_charges, car_types_late_drop_charges, car_types_night_charges, car_types_gst_charges
