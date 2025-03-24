function removeItem(productId) {
    // Hiển thị modal xác nhận xóa sản phẩm
    $('#removeModal').modal('show');

    // Đảm bảo sự kiện click được gán đúng cho nút xác nhận "Xóa"
    $('#confirmRemove').off('click').on('click', function() {
        // Điều hướng đến URL để xóa sản phẩm khỏi giỏ hàng
        window.location.href = `/cart/remove/${productId}/`;
    });
}

// Hàm định dạng số với dấu phẩy
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Hàm cập nhật số lượng sản phẩm
function updateQuantity(productId, change) {
    let quantityInput = $('#quantity_' + productId);  // Lấy đúng ô input của sản phẩm dựa trên productId
    let currentValue = parseInt(quantityInput.val());  // Lấy giá trị hiện tại của số lượng
    let newValue = currentValue + change;  // Tính số lượng mới

    if (newValue >= 1) {  // Chỉ cho phép số lượng >= 1
        quantityInput.val(newValue);  // Cập nhật giá trị vào ô input
        
        const price = parseFloat(quantityInput.data('price'));  // Lấy giá trị giá sản phẩm
        const total = price * newValue;  // Tính thành tiền mới

        $('#total_' + productId).text(formatNumber(total) + ' VND');  // Cập nhật thành tiền cho đúng sản phẩm

        // Tính tổng tiền của giỏ hàng
        calculateTotal();  // Gọi hàm tính tổng tiền sau khi cập nhật số lượng
    }
}


// Hàm tính tổng tiền của giỏ hàng
function calculateTotal() {
    let totalAmount = 0;

    $('.product-total').each(function() {
        const productTotal = parseFloat($(this).text().replace(/ VND/g, '').replace(/,/g, ''));  // Lấy thành tiền và loại bỏ dấu phẩy
        totalAmount += productTotal;  // Cộng thành tiền vào tổng tiền
    });

    $('#grand-total').text(formatNumber(totalAmount) + ' VND');  // Cập nhật tổng tiền hiển thị
}
