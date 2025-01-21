$(document).ready(function () {
    // Function to handle AJAX requests
    function handleAjaxRequest(url, data, successMessage, errorMessage, reloadSelector = null) {
        $.ajax({
            method: "POST",
            url: url,
            data: data,
            success: function (response) {
                console.log(response);
                alertify.success(successMessage || response.status);
                if (reloadSelector) {
                    $(reloadSelector).load(location.href + " " + reloadSelector);
                }
            },
            error: function () {
                alertify.error(errorMessage);
            }
        });
    }

    // Increment quantity
    $('.increment-btn').click(function (e) {
        e.preventDefault();

        let qtyInput = $(this).closest('.product_data').find('.qty-input');
        let value = parseInt(qtyInput.val(), 10) || 0;

        if (value < 10) {
            value++;
            qtyInput.val(value);
        } else {
            alertify.error("Maximum quantity reached.");
        }
    });

    // Decrement quantity
    $('.decrement-btn').click(function (e) {
        e.preventDefault();

        let qtyInput = $(this).closest('.product_data').find('.qty-input');
        let value = parseInt(qtyInput.val(), 10) || 0;

        if (value > 1) {
            value--;
            qtyInput.val(value);
        } else {
            alertify.error("Minimum quantity is 1.");
        }
    });

    // Add to Cart
    $('.addToCart').click(function (e) {
    e.preventDefault();

    let productData = $(this).closest('.product_data');
    let productId = productData.find('.prod_id').val();
    let productQty = productData.find('.qty-input').val();
    let csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        method: "POST",
        url: '/add-to-cart/',
        data: {
            product_id: productId,
            product_qty: productQty,
            csrfmiddlewaretoken: csrfToken,
        },
        success: function (response) {
            console.log(response);
            if (response.status) {
                alertify.success(response.status);
            } else {
                alertify.error('Something went wrong.');
            }
        },
        error: function () {
            alertify.error('Failed to add item to cart.');
        }
    });
});


    // Update Cart
    $('.update-cart-btn').click(function (e) {
        e.preventDefault();

        let productData = $(this).closest('.product_data');
        let productId = productData.find('.prod_id').val();
        let productQty = productData.find('.qty-input').val();
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        if (productId && productQty > 0) {
            handleAjaxRequest(
                '/update-cart/',
                {
                    product_id: productId,
                    product_qty: productQty,
                    csrfmiddlewaretoken: csrfToken,
                },
                "Cart updated successfully.",
                "Failed to update cart.",
                ".cartdata"
            );
        } else {
            alertify.error("Invalid product or quantity.");
        }
    });

    // Delete Cart Item
    $('.delete-cart-item').click(function (e) {
        e.preventDefault();

        let productData = $(this).closest('.product_data');
        let productId = productData.find('.prod_id').val();
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        if (productId) {
            handleAjaxRequest(
                '/delete-cart-item/',
                {
                    product_id: productId,
                    csrfmiddlewaretoken: csrfToken,
                },
                "Item removed from cart.",
                "Failed to delete item from cart.",
                ".cartdata"
            );
        } else {
            alertify.error("Invalid product.");
        }
    });

    // Add to Wishlist
    $('.addtowishlist').click(function (e) {
        e.preventDefault();

        let productData = $(this).closest('.product_data');
        let productId = productData.find('.prod_id').val();
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        if (productId) {
            handleAjaxRequest(
                '/add-to-wishlist/',
                {
                    product_id: productId,
                    csrfmiddlewaretoken: csrfToken,
                },
                "Item added to wishlist.",
                "Failed to add item to wishlist."
            );
        } else {
            alertify.error("Invalid product.");
        }
    });

    // Delete Wishlist Item
    $('.delete-wishlist-item').click(function (e) {
        e.preventDefault();

        let productData = $(this).closest('.product_data');
        let productId = productData.find('.prod_id').val();
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        if (productId) {
            handleAjaxRequest(
                '/delete-wishlist-item/',
                {
                    product_id: productId,
                    csrfmiddlewaretoken: csrfToken,
                },
                "Item removed from wishlist.",
                "Failed to delete item from wishlist.",
                ".wishdata"
            );
        } else {
            alertify.error("Invalid product.");
        }
    });
});
