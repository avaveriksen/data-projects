function [fittedmodel, gof] = fitcar3(table)
    % Non normalized and does not take new price into account

    km = table.("Kilometers");
    price = table.("Price");

    % Define a custom exponential model
    ft = fittype('a*exp(b*km)', 'independent', {'km'}, 'dependent', 'price');
    opts = fitoptions('Method', 'NonlinearLeastSquares');
    opts.StartPoint = [220000,-0.0001]; % Example guesses
    opts.Lower = [0, -Inf];                % Price must be positive
    opts.Upper = [Inf, 0];                    % Exponents negative (decaying)
    
    % Fit the model
    [fittedmodel, gof] = fit([km], price, ft, opts);

end