
function [fittedmodel, gof] = fitcar(table)
    km = table.("Kilometers");
    age = table.("Age");
    price = table.("Price");
    pricenew = table.("PriceNew");

    % Normalization
    price = price ./ pricenew;

    % Define a custom exponential model
    ft = fittype('exp(b*km + c*age)', 'independent', {'km', 'age'}, 'dependent', 'price');
    opts = fitoptions('Method', 'NonlinearLeastSquares');
    opts.StartPoint = [-0.0001, -0.0001]; % Example guesses
    opts.Lower = [-Inf, -Inf];                % Price must be positive
    opts.Upper = [0, 0];                    % Exponents negative (decaying)
    
    % Fit the model
    [fittedmodel, gof] = fit([km, age], price, ft, opts);

end