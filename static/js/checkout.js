$(document).ready(function () {
    $(".payWithRazopay").click(function (e) { 
        e.preventDefault();
        var fname = $("[name='fname']").val();
        var lname = $("[name='lname']").val();
        var email = $("[name='email']").val();
        var phone_no = $("[name='phone_no']").val();
        var address = $("[name='address']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var city = $("[name='city']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        if(fname == "" || lname == "" || email == "" || phone_no == "" || address == "" || country == "" || pincode == "" || city == "")
        {
            swal("Alert!","All fields are mandatory","error");
            return false;
        }
        else
        {
            $.ajax({
                method: "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    var options = {
                        "key": "rzp_test_Esqvlpm1Ro09bC", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_shipping_price*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Anant Jha", //your business name
                        "description": "Test Transaction",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb){
                            // alert(responseb.razorpay_payment_id);
                            data={
                                "fname":fname,
                                "lname":lname,
                                "email":email,
                                "phone_no":phone_no,
                                "address":address,
                                "country":country,
                                "pincode":pincode,
                                "city":city,
                                "payment_mode":"Paid by Razorpay",
                                "payment_id":responseb.razorpay_payment_id,
                                csrfmiddlewaretoken:token,
                            }
                            $.ajax({
                                method: "POST",
                                url: "/place-order",
                                data:data,
                                success: function(responsec){
                                    swal("Congratulations!",responsec.status,"success").then((value) => {
                                        window.location.href = '/my-orders'
                                    });
                                }
                            });
                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information especially their phone number
                            "name": fname+" "+lname , //your customer's name
                            "email": email,
                            "contact": phone_no //Provide the customer's phone number for better conversion rates 
                        },
                        "notes": {
                            "address": "Razorpay Corporate Office"
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();
                }
            });
        }
    });
});