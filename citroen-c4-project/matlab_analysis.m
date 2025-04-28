file = '/home/anders-eriksen/Documents/GitHub/data-projects/citroen-c4-project/bilbasen_scrape.csv'
opts = detectImportOptions(file)
cars = readtable(file,opts)

km = cars.Kilometers;
price = cars.Price_DKK_;

figure(1)
plot(km, price, '*')
grid on

year = string(cars.Year)
year = datetime(year, 'InputFormat', 'M/yyyy')

plot(year, price, 'o')
grid on

% Create a table for easier fitting
data = table(km(:), age(:), price(:), 'VariableNames', {'km', 'age', 'price'});

% Define a custom exponential model
ft = fittype('a * exp(b*km + c*age)', 'independent', {'km', 'age'}, 'dependent', 'price');
opts = fitoptions('Method', 'NonlinearLeastSquares');
opts.StartPoint = [10000, -0.0001, -0.0001]; % Example guesses
opts.Lower = [0, -Inf, -Inf];                % Price must be positive
opts.Upper = [Inf, 0, 0];                    % Exponents negative (decaying)

% Fit the model
[fittedmodel, gof] = fit([data.km, data.age], data.price, ft, opts);

% Plot
plot(fittedmodel, [data.km, data.age], data.price)
xlabel('Kilometers driven')
ylabel('Age')
zlabel('Price')
