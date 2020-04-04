# Orders are released to the production floor/shop floor periodically
# Every step of the simulation, the order release mechanism attempts to release orders according to certain rules
# The release mechanism might release any number of orders from the order pool, or none
from src import global_settings, environment


# CURRENTLY NOT IN USE
def sort_order_pool_by_due_date():
    print("order pool element 0 due date:" + str(environment.order_pool[0].due_date))
    environment.order_pool.sort(key=lambda x: x.due_date, reverse=False)
    print("order pool sorted by due date")
    print("order pool element 0 due date:" + str(environment.order_pool[0].due_date))
    return


# Immediate release policy: (THIS IS ACTUALLY PERIODIC RELEASE)
def release_using_immediate_release():
    # Each element in the order_pool gets moved to wip_A
    temporary_list = environment.order_pool.copy()
    temp_number_of_released_orders = 0
    for order_element in temporary_list:
        environment.wip_A.append(environment.order_pool.pop(environment.order_pool.index(order_element)))
        temp_number_of_released_orders += 1
    # debug info:
    if temp_number_of_released_orders > 0 and global_settings.show_order_release == True:
        print("Step " + str(global_settings.current_time) + ": " + str(temp_number_of_released_orders) + " orders released. Orders in pool: " + str(len(
            environment.order_pool)))
    return


# Timebucketing policy
def release_using_timebucketing(order_pool):
    test = 2
    return


def release_orders():
    # sort_order_pool_by_due_date()
    if global_settings.order_release_policy == "immediate_release":
        release_using_immediate_release()

    elif global_settings.order_release_policy == "timebucketing":
        release_using_timebucketing() # NOT YET IMPLEMENTED
    return
