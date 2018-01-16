import matplotlib.pyplot as plt
import numpy

def calc_mean(list_values):
	pre_mean = 0
	for x in list_values:
		pre_mean = pre_mean + x
		
	return (pre_mean / len(list_values))
	
	
def sum_of_squared_errors(list_values, mean):
	sse = 0
	for x in list_values:
		sse = sse + (x-mean)**2
		
	return sse
	
	
def sum_of_multiplied_xy(list_values_x, list_values_y, x_mean, y_mean):
	smxy = 0
	for i in range(0, len(list_values_x)):
		smxy = smxy + (list_values_x[i] - x_mean)*(list_values_y[i] - y_mean)
		
	return smxy
	
	
def cov(x, y):
    x_mean = calc_mean(x)
    y_mean = calc_mean(y)
    data = [(x[i] - x_mean) * (y[i] - y_mean)
            for i in range(len(x))]
    return sum(data) / (len(data) - 1)
	
	
def var(values, average):
    variance = 0
    for number in values:
        variance += (average - number) ** 2
    return variance / len(values)
	
	

if __name__ == "__main__":
	x_values = [1, 4, 4, 5]
	y_values = [3, 6, 8, 2]
	x_mean = calc_mean(x_values)
	y_mean = calc_mean(y_values)
	
	
	SSE = sum_of_squared_errors(y_values, y_mean) #changes made here
	SMXY = sum_of_multiplied_xy(x_values, y_values, x_mean, y_mean)
	
	slope = SSE / SMXY
	slope_2 = cov(x_values, y_values) / var(x_values, x_mean)
	
	b = y_mean - (slope_2 * x_mean)
	
	print("m = %.2f\nb = %.2f" % (slope_2, b))
	
	plt.plot(x_values, y_values, "ro")
	x = numpy.array(x_values)
	y = slope_2*x+b
	plt.plot(x, y)
	#plt.axis([0, 6, 0, 5])
	plt.show()
	
	
	
	