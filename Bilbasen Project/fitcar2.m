function [fittedmodel, gof] = fitcar2(table)
    % Non normalized and does not take new price into account

    km = table.("Kilometers");
    age = table.("Age");
    price = table.("Price");

    % Define a custom exponential model
    ft = fittype('a*exp(b*km + c*age)', 'independent', {'km', 'age'}, 'dependent', 'price');
    opts = fitoptions('Method', 'NonlinearLeastSquares');
    opts.StartPoint = [220000,-0.0001, -0.0001]; % Example guesses
    opts.Lower = [0, -Inf, -Inf];                % Price must be positive
    opts.Upper = [Inf, 0, 0];                    % Exponents negative (decaying)
    
    % Fit the model
    [fittedmodel, gof] = fit([km, age], price, ft, opts);

end