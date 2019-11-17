import simpy
import random
import numpy

NO_OF_CUSTOMERS = 20
NO_OF_CASHIERS = 2
NO_OF_BARISTAS = 3

menu = {1:["Regular Coffee",10,15], 2:["Latte",30,45],
        3:["Mocha",30,45], 4:["Cold Brew",10,20], 5:["Frappe",50,70],
        6:["Espresso",20,35]}
payment_options = {1:["Cash",15,30], 2:["Card",10,20]}

payment_wait_time = []  #list to hold the time until a cashier is available
payment_time = []       #list to hold the time taken to make payments
order_wait_time = []    #list to hold te time until a barista is available
order_time = []         #list to hold the time taken to prepare the order

def generate_customer(env, cashier, barista):
    for i in range(NO_OF_CUSTOMERS):
        yield env.timeout(random.randint(1,20))
        env.process(customer(env, i, cashier, barista))


def customer(env, name, cashier, barista):
    print("Customer %s arrived at time %.1f" % (name, env.now))
    with cashier.request() as req:
        start_cq = env.now
        yield req
        payment_wait_time.append(env.now - start_cq)
        menu_item = random.randint(1, 6)
        payment_type = random.randint(1, 2)
        time_to_order = random.randint(payment_options[payment_type][1], payment_options[payment_type][2])
        payment_name = payment_options[payment_type][0]
        yield env.timeout(time_to_order)
        print("> > > Customer %s finished paying by %s in %.1f seconds" % (name, payment_name, env.now - start_cq))
        payment_time.append(env.now - start_cq)

    with barista.request() as req:
        start_bq = env.now
        yield req
        order_wait_time.append(env.now - start_bq)
        time_to_prepare = random.randint(menu[menu_item][1], menu[menu_item][2])
        item_name = menu[menu_item][0]
        yield env.timeout(time_to_prepare)
        print(">> >> >> Customer %s served %s in %.1f seconds" % (name, item_name, env.now - start_cq))
        order_time.append(env.now - start_cq)


env = simpy.Environment()
cashier = simpy.Resource(env, NO_OF_CASHIERS)
barista = simpy.Resource(env, NO_OF_BARISTAS)

env.process(generate_customer(env, cashier, barista))
env.run(until=400)

print("\n\nWITH %s CASHIERS and %s BARISTAS and %s SERIALLY ARRIVING CUSTOMERS..." % (NO_OF_CASHIERS, NO_OF_BARISTAS, NO_OF_CUSTOMERS))
print("Average wait time in payment queue: %.1f seconds." % (numpy.mean(payment_wait_time)))
print("Average time until making the payment: %.1f seconds." % (numpy.mean(payment_time)))
print("Average wait time in order queue: %.1f seconds." % (numpy.mean(order_wait_time)))
print("Average time until order is serviced: %.1f seconds." % (numpy.mean(order_time)))