from src import global_settings, environment


# Move orders for shop_type == flow_shop
def move_orders_flow_shop():
    """
    Move orders from WIPs to machines, from machines to WIPs and finally to finished/shipped goods inventories.
    The routing for each order depends on the order's product type.
    :return: this function returns nothing
    """
    # All orders from order_pool to WIP_A
    # All orders from WIP_A to M_A
    # if product_type 1,2,3 then to WIP_B
    # if product type 4,5,6 then to WIP_C
    # all from WIP_B to M_B
    # all from WIP_C to M_C
    # if product type 1 or 4, then to WIP_D
    # if product type 2 or 5, then to WIP_E
    # if product type 3 or 6, then to WIP_F
    # all to FGI

    ##################### Step 1: empty the machines that have finished production in the previous step

    # Move order from machine_A to WIP_B or WIP_C, if processing_time_remaining of order is 0
    if len(environment.machine_A.orders_inside_the_machine) == 1:
        if environment.machine_A.orders_inside_the_machine[0].processing_time_remaining == 0:
            environment.machine_A.orders_inside_the_machine[0].arrival_prodstep_2_wip = global_settings.current_time

            if environment.machine_A.orders_inside_the_machine[0].product_type in (1, 2, 3):
                if global_settings.show_machine_output == True:
                    print("Step " + str(global_settings.current_time) + ": Machine_A: order finished. orderID: " +
                          str(environment.machine_A.orders_inside_the_machine[0].orderID) + " || product type: "
                          + str(environment.machine_A.orders_inside_the_machine[0].product_type))
                environment.wip_B.append(environment.machine_A.orders_inside_the_machine.pop(0))

            elif environment.machine_A.orders_inside_the_machine[0].product_type in (4, 5, 6):
                if global_settings.show_machine_output == True:
                    print("Step " + str(global_settings.current_time) + ": Machine_A: order finished. orderID: " +
                          str(environment.machine_A.orders_inside_the_machine[0].orderID) + " || product type: "
                          + str(environment.machine_A.orders_inside_the_machine[0].product_type))
                environment.wip_C.append(environment.machine_A.orders_inside_the_machine.pop(0))
            else:
                raise ValueError("No product_type assigned in machine A")

    # Move order from machine_B to WIP D/E/F, depending on product type
    list_of_product_types = [1, 2, 3]
    list_of_wips = [environment.wip_D, environment.wip_E, environment.wip_F]
    orders = environment.machine_B.orders_inside_the_machine
    if len(orders) == 1:
        if orders[0].processing_time_remaining == 0:
            orders[0].arrival_prodstep_3_wip = global_settings.current_time
            for product_Type in list_of_product_types:
                if orders[0].product_type == product_Type:
                    if global_settings.show_machine_output == True:
                        print("Step " + str(global_settings.current_time) + ": Machine_B: order finished. " +
                              "orderID: " + str(orders[0].orderID) +
                              " || product type: " + str(orders[0].product_type))
                    list_of_wips[list_of_product_types.index(product_Type)].append(orders.pop(0))
                    break

    # # Move order from machine_C to WIP D/E/F, depending on product type
    list_of_product_types = [4, 5, 6]
    list_of_wips = [environment.wip_D, environment.wip_E, environment.wip_F]
    orders = environment.machine_C.orders_inside_the_machine
    if len(orders) == 1:
        if orders[0].processing_time_remaining == 0:
            orders[0].arrival_prodstep_3_wip = global_settings.current_time
            for product_Type in list_of_product_types:
                if orders[0].product_type == product_Type:
                    if global_settings.show_machine_output == True:
                        print("Step " + str(global_settings.current_time) + ": Machine_C: order finished. " +
                              "orderID: " + str(orders[0].orderID) +
                              " || product type: " + str(orders[0].product_type))
                    list_of_wips[list_of_product_types.index(product_Type)].append(orders.pop(0))
                    break

    # Move order from machine_D/E/F to FGI
    list_of_machines = [environment.machine_D, environment.machine_E, environment.machine_F]
    for machine in list_of_machines:
        if len(machine.orders_inside_the_machine) == 1:
            if machine.orders_inside_the_machine[0].processing_time_remaining == 0:
                if global_settings.show_machine_output == True:
                    print("Step " + str(global_settings.current_time) + ": " + str(
                        machine.name) + ": order finished. " +
                          "orderID: " + str(machine.orders_inside_the_machine[0].orderID) +
                          " || product type: " + str(machine.orders_inside_the_machine[0].product_type))

                machine.orders_inside_the_machine[0].finished_production_date = global_settings.current_time
                environment.finished_goods_inventory.append(
                    machine.orders_inside_the_machine.pop(0))

    ##################### Step 2: we move orders from WIPs into the machines
    # Each origin belongs to one destination.
    # The first item in destinations belongs to the first item in origins and so on.
    # The order movements shown in Step 2 do not depend on the order's product type,
    # instead they depend on the machine scheduling policy.
    # In this version, only a first come, first serve policy is implemented.
    list_of_destinations = environment.list_of_all_machines
    list_of_origins = environment.list_of_all_wip_elements
    wip_names = ["wip_A", "wip_B", "wip_C", "wip_D", "wip_E", "wip_F"]

    for machine in list_of_destinations:
        if global_settings.scheduling_policy == "first_come_first_serve" and \
                len(machine.orders_inside_the_machine) == 0 and \
                len(list_of_origins[list_of_destinations.index(machine)]) > 0:

            ############ debugging info ############
            if global_settings.show_movements_from_wip_to_machine == True:
                print("Step " + str(
                    global_settings.current_time) + ": Order moved from " +
                      wip_names[list_of_destinations.index(machine)] + " to " + str(
                    machine.name) + ". Orders in " +
                      wip_names[list_of_destinations.index(machine)] + ": " + str(
                    len(list_of_origins[list_of_destinations.index(machine)])))
            ########################
            machine.orders_inside_the_machine.append(list_of_origins[list_of_destinations.index(machine)].pop(0))
            environment.set_new_random_processing_time(machine)  # set a new random processing time for the next order
            # if machine.name == "Machine A":
            #     with open('m1.csv', mode='a') as m1_CSV:
            #         results_writer = csv.writer(m1_CSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #         results_writer.writerow([environment.machine_A.processing_time])

            machine.orders_inside_the_machine[0].processing_time_remaining = machine.processing_time
            machine.orders_inside_the_machine[0].arrival_times_m1m2m3.append(global_settings.current_time)

    ##################### Step 3: move orders from FGI to shipped when order due date is reached
    # Move orders from FGI to shipped_orders once they have reached their due_date
    # Calculate lateness for each order
    if len(environment.finished_goods_inventory) > 0:
        for order_element in environment.finished_goods_inventory:
            if order_element.due_date <= global_settings.current_time:
                order_element.shipping_date = global_settings.current_time
                # Calculate lateness/earliness of order:
                if order_element.shipping_date > order_element.due_date:
                    order_element.lateness = order_element.shipping_date - order_element.due_date
                else:
                    order_element.earliness = order_element.shipping_date - order_element.finished_production_date
                # Calculate flow time of order:
                order_element.flow_time = order_element.finished_production_date - order_element.order_release_date
                # Optional debugging info:
                if global_settings.show_order_shipping == True:
                    print("Step " + str(global_settings.current_time) + ": Shipped orderID " +
                          str(order_element.orderID) + " with due date " + str(
                        order_element.due_date) + " Lateness: " + str(order_element.lateness))
                # Move order from FGI to shipped goods inventory
                environment.shipped_orders.append(
                    environment.finished_goods_inventory.pop(
                        environment.finished_goods_inventory.index(order_element)))

    return


# Move orders for shop_type == flow_shop
def move_orders_job_shop():
    """
    Move orders from WIPs to machines, from machines to WIPs and finally to finished/shipped goods inventories.
    The routing for each order depends on the order's product type.
    :return: this function returns nothing
    """
    # First: Move order from order_pool to the respective WIP
    # Second: route products as shown below
    # P1: M1-M2-M3
    # P2: M1-M3-M2
    # P3: M2-M1-M3
    # P4: M2-M3-M1
    # P5: M3-M1-M2
    # P6: M3-M2-M1
    # Third: after production is done, move order to FGI

    ##################### Step 1: empty the machines that have finished production in the previous step
    list_of_product_types = [1, 2, 3, 4, 5, 6]
    list_of_destinations = [
        [environment.wip_B, environment.wip_C, environment.finished_goods_inventory],
        [environment.wip_C, environment.wip_B],
        [environment.wip_A, environment.wip_C],
        [environment.wip_C, environment.wip_A],
        [environment.wip_A, environment.wip_B],
        [environment.wip_B, environment.wip_A]
    ]
    list_of_process_steps = [0,1,2,3]
    # Move order from machine to the next wip, if processing_time_remaining of order is 0
    for machine_element in environment.list_of_all_machines:
        orders = machine_element.orders_inside_the_machine
        if len(orders) == 1:
            if orders[0].processing_time_remaining == 0:

                ##### example case product type 1, step 0:
                # von destinations nehme list item 0 (prodtype)
                # von list item 0 nehme list item 0 (prodstep)
                # füge da die order ein

                orders[0].current_production_step += 1



                for product_Type in list_of_product_types:
                    if orders[0].product_type == product_Type:
                        # if global_settings.show_machine_output == True:
                        #     print("Step " + str(global_settings.current_time) + ": Machine_B: order finished. " +
                        #           "orderID: " + str(orders[0].orderID) +
                        #           " || product type: " + str(orders[0].product_type))
                        list_of_destinations[list_of_product_types.index(product_Type)].append(orders.pop(0))
                        #

    ##################### Step 2: move orders from WIPs into the machines
    # Each origin belongs to one destination.
    # The first item in destinations belongs to the first item in origins and so on.
    # The order movements shown in Step 2 do not depend on the order's product type,
    # instead they depend on the machine scheduling policy.
    # In this version, only a first come, first serve policy is implemented.
    list_of_destinations = environment.list_of_all_machines
    list_of_origins = environment.list_of_all_wip_elements
    wip_names = ["wip_A", "wip_B", "wip_C", "wip_D", "wip_E", "wip_F"]

    for machine in list_of_destinations:
        if global_settings.scheduling_policy == "first_come_first_serve" and \
                len(machine.orders_inside_the_machine) == 0 and \
                len(list_of_origins[list_of_destinations.index(machine)]) > 0:

            ############ debugging info ############
            if global_settings.show_movements_from_wip_to_machine == True:
                print("Step " + str(
                    global_settings.current_time) + ": Order moved from " +
                      wip_names[list_of_destinations.index(machine)] + " to " + str(
                    machine.name) + ". Orders in " +
                      wip_names[list_of_destinations.index(machine)] + ": " + str(
                    len(list_of_origins[list_of_destinations.index(machine)])))
            ########################
            machine.orders_inside_the_machine.append(list_of_origins[list_of_destinations.index(machine)].pop(0))
            environment.set_new_random_processing_time(machine)  # set a new random processing time for the next order
            machine.orders_inside_the_machine[0].processing_time_remaining = machine.processing_time
            machine.orders_inside_the_machine[0].arrival_times_m1m2m3.append(global_settings.current_time)

    ##################### Step 3: move orders from FGI to shipped when order due date is reached
    # Move orders from FGI to shipped_orders once they have reached their due_date
    # Calculate lateness for each order
    if len(environment.finished_goods_inventory) > 0:
        for order_element in environment.finished_goods_inventory:
            if order_element.due_date <= global_settings.current_time:
                order_element.shipping_date = global_settings.current_time
                order_element.current_production_step = None
                # Calculate lateness/earliness of order:
                if order_element.shipping_date > order_element.due_date:
                    order_element.lateness = order_element.shipping_date - order_element.due_date
                else:
                    order_element.earliness = order_element.shipping_date - order_element.finished_production_date
                # Calculate flow time of order:
                order_element.flow_time = order_element.finished_production_date - order_element.order_release_date
                # Optional debugging info:
                if global_settings.show_order_shipping == True:
                    print("Step " + str(global_settings.current_time) + ": Shipped orderID " +
                          str(order_element.orderID) + " with due date " + str(
                        order_element.due_date) + " Lateness: " + str(order_element.lateness))
                # Move order from FGI to shipped goods inventory
                environment.shipped_orders.append(
                    environment.finished_goods_inventory.pop(
                        environment.finished_goods_inventory.index(order_element)))
    return

# def backup():
#     if len(environment.machine_A.orders_inside_the_machine) == 1:
#         if environment.machine_A.orders_inside_the_machine[0].processing_time_remaining == 0:
#             environment.machine_A.orders_inside_the_machine[0].arrival_prodstep_2_wip = global_settings.current_time
#
#             if environment.machine_A.orders_inside_the_machine[0].product_type in (1, 2, 3):
#                 if global_settings.show_machine_output == True:
#                     print("Step " + str(global_settings.current_time) + ": Machine_A: order finished. orderID: " +
#                           str(environment.machine_A.orders_inside_the_machine[0].orderID) + " || product type: "
#                           + str(environment.machine_A.orders_inside_the_machine[0].product_type))
#                 environment.wip_B.append(environment.machine_A.orders_inside_the_machine.pop(0))
#
#             elif environment.machine_A.orders_inside_the_machine[0].product_type in (4, 5, 6):
#                 if global_settings.show_machine_output == True:
#                     print("Step " + str(global_settings.current_time) + ": Machine_A: order finished. orderID: " +
#                           str(environment.machine_A.orders_inside_the_machine[0].orderID) + " || product type: "
#                           + str(environment.machine_A.orders_inside_the_machine[0].product_type))
#                 environment.wip_C.append(environment.machine_A.orders_inside_the_machine.pop(0))
#             else:
#                 raise ValueError("No product_type assigned in machine A")
#
#     # Move order from machine_B to WIP D/E/F, depending on product type
#
#
# list_of_product_types = [1, 2, 3]
# list_of_wips = [environment.wip_D, environment.wip_E, environment.wip_F]
# orders = environment.machine_B.orders_inside_the_machine
# if len(orders) == 1:
#     if orders[0].processing_time_remaining == 0:
#         orders[0].arrival_prodstep_3_wip = global_settings.current_time
#         for product_Type in list_of_product_types:
#             if orders[0].product_type == product_Type:
#                 if global_settings.show_machine_output == True:
#                     print("Step " + str(global_settings.current_time) + ": Machine_B: order finished. " +
#                           "orderID: " + str(orders[0].orderID) +
#                           " || product type: " + str(orders[0].product_type))
#                 list_of_wips[list_of_product_types.index(product_Type)].append(orders.pop(0))
#                 break
#
# # # Move order from machine_C to WIP D/E/F, depending on product type
# list_of_product_types = [4, 5, 6]
# list_of_wips = [environment.wip_D, environment.wip_E, environment.wip_F]
# orders = environment.machine_C.orders_inside_the_machine
# if len(orders) == 1:
#     if orders[0].processing_time_remaining == 0:
#         orders[0].arrival_prodstep_3_wip = global_settings.current_time
#         for product_Type in list_of_product_types:
#             if orders[0].product_type == product_Type:
#                 if global_settings.show_machine_output == True:
#                     print("Step " + str(global_settings.current_time) + ": Machine_C: order finished. " +
#                           "orderID: " + str(orders[0].orderID) +
#                           " || product type: " + str(orders[0].product_type))
#                 list_of_wips[list_of_product_types.index(product_Type)].append(orders.pop(0))
#                 break
#
# # Move order from machine_D/E/F to FGI
# list_of_machines = [environment.machine_D, environment.machine_E, environment.machine_F]
# for machine in list_of_machines:
#     if len(machine.orders_inside_the_machine) == 1:
#         if machine.orders_inside_the_machine[0].processing_time_remaining == 0:
#             if global_settings.show_machine_output == True:
#                 print("Step " + str(global_settings.current_time) + ": " + str(
#                     machine.name) + ": order finished. " +
#                       "orderID: " + str(machine.orders_inside_the_machine[0].orderID) +
#                       " || product type: " + str(machine.orders_inside_the_machine[0].product_type))
#
#             machine.orders_inside_the_machine[0].finished_production_date = global_settings.current_time
#             environment.finished_goods_inventory.append(
#                 machine.orders_inside_the_machine.pop(0))
#
# ##################### Step 2: we move orders from WIPs into the machines
# # Each origin belongs to one destination.
# # The first item in destinations belongs to the first item in origins and so on.
# # The order movements shown in Step 2 do not depend on the order's product type,
# # instead they depend on the machine scheduling policy.
# # In this version, only a first come, first serve policy is implemented.
# list_of_destinations = environment.list_of_all_machines
# list_of_origins = environment.list_of_all_wip_elements
# wip_names = ["wip_A", "wip_B", "wip_C", "wip_D", "wip_E", "wip_F"]
#
# for machine in list_of_destinations:
#     if global_settings.scheduling_policy == "first_come_first_serve" and \
#             len(machine.orders_inside_the_machine) == 0 and \
#             len(list_of_origins[list_of_destinations.index(machine)]) > 0:
#
#         ############ debugging info ############
#         if global_settings.show_movements_from_wip_to_machine == True:
#             print("Step " + str(
#                 global_settings.current_time) + ": Order moved from " +
#                   wip_names[list_of_destinations.index(machine)] + " to " + str(
#                 machine.name) + ". Orders in " +
#                   wip_names[list_of_destinations.index(machine)] + ": " + str(
#                 len(list_of_origins[list_of_destinations.index(machine)])))
#         ########################
#         machine.orders_inside_the_machine.append(list_of_origins[list_of_destinations.index(machine)].pop(0))
#         environment.set_new_random_processing_time(machine)  # set a new random processing time for the next order
#         # if machine.name == "Machine A":
#         #     with open('m1.csv', mode='a') as m1_CSV:
#         #         results_writer = csv.writer(m1_CSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         #         results_writer.writerow([environment.machine_A.processing_time])
#
#         machine.orders_inside_the_machine[0].processing_time_remaining = machine.processing_time
#         machine.orders_inside_the_machine[0].arrival_times_m1m2m3.append(global_settings.current_time)
#
# ##################### Step 3: move orders from FGI to shipped when order due date is reached
# # Move orders from FGI to shipped_orders once they have reached their due_date
# # Calculate lateness for each order
# if len(environment.finished_goods_inventory) > 0:
#     for order_element in environment.finished_goods_inventory:
#         if order_element.due_date <= global_settings.current_time:
#             order_element.shipping_date = global_settings.current_time
#             # Calculate lateness/earliness of order:
#             if order_element.shipping_date > order_element.due_date:
#                 order_element.lateness = order_element.shipping_date - order_element.due_date
#             else:
#                 order_element.earliness = order_element.shipping_date - order_element.finished_production_date
#             # Calculate flow time of order:
#             order_element.flow_time = order_element.finished_production_date - order_element.order_release_date
#             # Optional debugging info:
#             if global_settings.show_order_shipping == True:
#                 print("Step " + str(global_settings.current_time) + ": Shipped orderID " +
#                       str(order_element.orderID) + " with due date " + str(
#                     order_element.due_date) + " Lateness: " + str(order_element.lateness))
#             # Move order from FGI to shipped goods inventory
#             environment.shipped_orders.append(
#                 environment.finished_goods_inventory.pop(
#                     environment.finished_goods_inventory.index(order_element)))
#
#     return


def move_orders():
    if global_settings.shop_type == "flow_shop":
        move_orders_flow_shop()
    elif global_settings.shop_type == "job_shop":
        move_orders_job_shop()
    return
