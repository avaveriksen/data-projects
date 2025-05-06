clear;clc;close all;

%% Load source image
%source = imread("colorful-bird.jpg");
%source = imread("mount-assiniboine-1.jpg");
%source = imread("mount_assiniboine_2.jpg");
source = imread("citroen-c4-grainy.jpg");

%% Display Source Image and export to directory
figure(1)
image(source);
axis off
exportgraphics(figure(1), 'source.png', 'Resolution', 300)

%[R, G, B] = getRGB(source, 1, 1);

%% Blur image for filtering of color spectrum
% blur radius
r = 2; %blur radius

% reduce image size to compute faster
small_im = reduce_image_size(source);
blurred = blur(small_im, r);

% export to directory
figure(2)
image(blurred);
axis off
exportgraphics(figure(2), 'source_blurred.png', 'Resolution', 300)

%% Split color spectrum to extract average RGB values
[means_R, means_G, means_B] = splitcolors(blurred);

%% Generate pallette of curated colors
pallette = create_pallette(means_R, means_G, means_B);


%% Functions
function reduced_image = reduce_image_size(im)
    im_dims = size(im);
    sorted_sizes = sort(im_dims);

    %Calculate scaling factor to get image width close to 500 pixels
    factor = ceil(sorted_sizes(2) / 500);
    
    % MATLAB function 'image' expects a 3-page array of type uint8
    reduced_image = uint8(im(1:factor:end, 1:factor:end, :));
end


function blurred = blur(source, r)
    % blurs pictures with a provided radius 'r'
    % This function removes the r outermost pixels
    [height, width,~] = size(source);
    
    %3D array to store blurred image
    blurred = zeros(height, width, 3);
    
    for col = 1+r:width-r
        for row = 1+r:height-r 
            % Extract cluster. Cluster is the [col, row] indexed pixel and
            % the r pixels around it
            cluster = source(row-r:row+r,col-r:col+r,:);
            
            for i = 1:3
                % load averaged values into img
                blurred(row, col, i) = floor(mean(mean(cluster(:, :, i))));
            end
        end
    end
    % Return uint8 type array with r outermost pixels removed
    blurred = uint8(blurred(r+1:height-r-1, r+1:width-r-1,:));
end

function [mean_R, mean_G, mean_B] = splitcolors(source)
    % Seperates the pixels out in colorspaces to extraxt average color
    % values
    
    % Get RGB values of all pixels in argument picture
    [height, width, ~] = size(source);
    split = height * width;
    R_values = source(1:split);
    G_values = source(1+split:2*split);
    B_values = source(1+2*split:3*split);
    
    % Preallocate dynamic arrays
    mean_R = [];
    mean_G = [];
    mean_B = [];
    dot_sizes = [];
    dot_colors = [];
    
    % Constant to leave out pixels if there are too few within a colorspace
    trim = 5;
    
    % Open figure and set hold on
    figure(3); clf; hold on
    
    % Color spaces are confined within intervals on the RGB axes RGB <--> XYZ.
    for R_i = 17:34:255
        for G_i = 17:34:255
            for B_i = 17:34:255
                % Using logical operators to determine what pixels belong
                % to current color space
                logic_R = R_values >= R_i-51 & R_values < R_i;
                logic_G = G_values >= G_i-51 & G_values < G_i;
                logic_B = B_values >= B_i-51 & B_values < B_i;
                logic_RGB = logic_R & logic_G & logic_B;
                % Indexes of pixels in current color space
                pixels_i = find(logic_RGB);
                
                % Compute colorspace if number of elements > trim
                if numel(pixels_i) > trim
                    % Calculate mean values
                    R_mean_val = mean(R_values(pixels_i));
                    G_mean_val = mean(G_values(pixels_i));
                    B_mean_val = mean(B_values(pixels_i));

                    % Store in dynamic array
                    mean_R(end+1) = floor(R_mean_val);
                    mean_G(end+1) = floor(G_mean_val);
                    mean_B(end+1) = floor(B_mean_val);

                    % Scatter color and dot sizes for plotting
                    scatter_color = [R_mean_val, G_mean_val, B_mean_val] / 255;
                    dot_colors(end + 1, 1:3) = scatter_color;
                    dot_sizes(end+1) = length(pixels_i) / (trim/2);
                end
            end
        end
    end
    
    % Scatter plot
    scatter3(mean_R, mean_G, mean_B, dot_sizes, dot_colors, 'filled');

    
    % Plot export
    f = figure(3);
    f.Color = [0 0 0];
    ax = findobj(f, 'Type', 'axes');
    ax.Color = [0 0 0];
    ax.XColor = [1 0 0];
    ax.YColor = [0 1 0];
    ax.ZColor = [0 0 1];
    ax.GridColor = [1 1 1];
    grid on
    ax.View = [13 10];
    ax.XLim = [0 255];
    ax.YLim = [0 255];
    ax.ZLim = [0 255];
    exportgraphics(f, 'avg_scatter.png', 'Resolution', 300, 'BackgroundColor', 'current');

    % Create and export large pallette with all average RGB colors
    n_colors = length(mean_R);
    h = 8;
    w = ceil(n_colors/h);
    big_pallette = uint8(ones(h, w, 3)*255);

    R = uint8(ones(h * w, 1) * 255);
    G = uint8(ones(h * w, 1) * 255); 
    B = uint8(ones(h * w, 1) * 255);

    R(1:n_colors) = mean_R;
    G(1:n_colors) = mean_G;
    B(1:n_colors) = mean_B;

    big_pallette(:, :, 1) = reshape(R, h, w);
    big_pallette(:,:,2) = reshape(G, h, w);
    big_pallette(:, :, 3) = reshape(B, h, w);

    imwrite(big_pallette, "big_pallette.png");
end

function pallette = create_pallette(R, G, B)
    % Creates a smaller pallette of curated colors, as well as a
    % corresponding set of colors with boosted HSV Value
    
    % create pixel array from means
    pallette(:, 1, 1) = R;
    pallette(:, 1, 2) = G;
    pallette(:, 1, 3) = B;

    pallette = uint8(pallette);
    
    % number of colors in pallette
    n_pallette = length(pallette);
    
    % anchor colors, of which there are 14, corresponding to corners + sides of a box
    anchors = zeros(14, 1, 3);
    anchors([1, 2, 3, 4, 13], 1, 1) = 255;
    anchors([2, 4, 6, 8, 14], 1, 2) = 255;
    anchors([3, 4, 7, 8, 12], 1, 3) = 255;
    anchors([9, 11, 12, 14], 1, 1) = 127;
    anchors([9, 10, 12, 13], 1, 2) = 127;
    anchors([10, 11, 13, 14], 1, 3) = 127;

    % Get pallette colors spatial proximity to anchor colors
    prox_lut = zeros(14, n_pallette);
    for i = 1:14
        x(1:3) = anchors(i, 1, :);
        for j = 1:n_pallette
            y(1:3) = pallette(j, 1, :);
            prox_lut(i, j) = norm(double(x)-double(y));
        end
    end
    
    %value to replace lut values with 
    x = ceil(max(max(prox_lut)));
    
    curated_i(14) = 0;
    new_i = 0;
    
    % The curated colors are the colors closest in proximity to each of the
    % anchor colors, with colors interpreted as points in a 3D coordinate
    % system
    for i = 1:14
        new_i = find(prox_lut(i, :) == min(prox_lut(i, :)), 1);
        curated_i(i) = new_i;
        prox_lut(:, new_i) = x;
    end

    pallette = pallette(curated_i, 1, :);
    
    % Calculating the boosted colors
    V_boost = zeros(length(pallette),1, 3);

    for i = 1:length(V_boost)
        ref = max(pallette(i, :)); % get the highest R, G or B
        sf = 255 / double(ref); % calculate scaling factor to boost that to 255
        V_boost(i, 1, :) = uint8(double(pallette(i, 1, :)) * sf); % scale R, G and B with sf
    end
    
    % Adding boosted colors to pallette
    pallette(:, 2, :) = V_boost;
    
    % Export
    imwrite(pallette, "pallette.png");

end
