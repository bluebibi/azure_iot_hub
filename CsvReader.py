import csv


def get_values_from_file(filename = 'data0.csv'):
    torque = []
    displacement = []
    velocity = []
    acceleration = []

    with open('./data/' + filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            torque.append(float(row[1].strip()))
            displacement.append(float(row[2].strip()))
            velocity.append(float(row[3].strip()))
            acceleration.append(float(row[4].strip()))

    return torque, displacement, velocity, acceleration