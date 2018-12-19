import pandas as pd
import numpy as np
import statsmodels.api as sm

indeed_US = pd.read_csv("newData.csv")

modelColumns = ['clicks', 'estimatedSalary', 'jobAgeDays']
High_School = pd.DataFrame(columns = modelColumns)
Higher_ed = pd.DataFrame(columns = modelColumns)
No_ed = pd.DataFrame(columns = modelColumns)

High_School['estimatedSalary'] = indeed_US['High School Salary']
High_School['clicks'] = indeed_US['High School Clicks']
High_School['jobAgeDays'] = indeed_US['High School Length']
Higher_ed['estimatedSalary'] = indeed_US['Higher Ed Salary']
Higher_ed['clicks'] = indeed_US['Higher Ed Clicks']
Higher_ed['jobAgeDays'] = indeed_US['Higher Ed Length']
No_ed['estimatedSalary'] = indeed_US['No Ed Salary']
No_ed['clicks'] = indeed_US['No Ed Clicks']
No_ed['jobAgeDays'] = indeed_US['No Ed Length']

High_School = High_School[np.isfinite(High_School['jobAgeDays'])]
Higher_ed = Higher_ed[np.isfinite(Higher_ed['jobAgeDays'])]
No_ed = No_ed[np.isfinite(No_ed['jobAgeDays'])]

X_high = High_School['estimatedSalary']
y_high = High_School['jobAgeDays']

#high_reg = linear_model.LinearRegression()
#higher_reg = linear_model.LinearRegression()
#none_reg = linear_model.LinearRegression()

high_model = sm.OLS(y_high, X_high).fit()
predictions_high = high_model.predict(X_high)
#pyplot.scatter(X_high, y_high)
#pyplot.plot(X_high, predictions_high)
print("HIGH SCHOOL")
print(high_model.summary())
#pyplot.show()
#savefig('High_School.png')

X_higher = Higher_ed['estimatedSalary']
y_higher = Higher_ed['jobAgeDays']

higher_model = sm.OLS(y_higher, X_higher).fit()
predictions_higher = higher_model.predict(X_higher)
#pyplot.scatter(X_higher, y_higher)
#pyplot.plot(X_higher, predictions_higher)
print("HIGHER EDUCATION")
print(higher_model.summary())
#pyplot.show()
#savefig('Higher_Education.png')

X_none = No_ed['estimatedSalary']
y_none = No_ed['jobAgeDays']

none_model = sm.OLS(y_none, X_none).fit()
predictions_none = none_model.predict(X_none)
#pyplot.scatter(X_none, y_none)
#pyplot.plot(X_none, predictions_none)
print("NO EDUCATION")
print(none_model.summary())
#pyplot.show()
#savefig('No_Education.png')

#X = sm.add_constant(X)

