/* ----- Initialize api sdk ----- */
var apigClient = apigClientFactory.newClient();

$(document).ready(function () {

    /* ----- configure the user data ----- */
    var awsRegion = 'us-east-1';
    var identityPoolId = 'us-east-1:278287f5-8765-46a7-baf1-5f31e9c8686e';
   

    /* ----- Getting AWS credentials ----- */
    // Initialize the Amazon Cognito credentials provider
    AWS.config.region = awsRegion;
    AWS.config.credentials = new AWS.CognitoIdentityCredentials({
        IdentityPoolId: identityPoolId
    });

    /* ----- Exchange credentials ----- */


    //  initialize SDK with credentials to sign the API calls
    apigClient = apigClientFactory.newClient({
        accessKey: "ASIA2UJLLBTLABINX45I",
        secretKey: "eCPhtcSMcsLbfMx5R7BA9cbG0aV4C9DDGDFHhmkj",
        sessionToken: "FQoGZXIvYXdzEFEaDJVrey0zlvncfCKwxyL9ASrqpmffJ75nx8A0Q0okYyEkzrJRdJ5MXo0ZLB0PVkTx8uDmNyWVdnaNv2EBKmdARoyo2LBRdL9zEEslaWVFtRuWxrYzGXFmiV0iQ8/k0sZStBdesq1oG9xNDXTM4+VTb30hYi/XVZV0ngvXybehl/bh54dOl2quqckKsUowZ0v2yNmNocAQG+OE0X0VztIEEVjL4CilPXm1iVoMLD1tCYOi5E1BxT+A4q9KtAWSlyv6YwLIBy/KJVeJhPXwx8Sh1+wAPc0Py0wWaEkudvtsu8SadK84vXWipQhXM5nHCOXdx5D7SogEdzzH/cc4Uk7dg+K/yBy8GhV5hb6Xesko+Nej7AU="
    });

    /* -----  Calling API----- */
    function callOTPApi(otpInput) {
        // The three parameters passed to api call are:
        // params, body, additionalParams
        // params and additionalParams = {}

        return apigClient.formPost({
        }, {
            messages: [{
                type: 'unstructured',
                unstructured: {
                    text: otpInput
                }
            }]
        }, {});
    }

    /* ----- Send the message to backend and display response ----- */
    function submitOTP() {
        otpInput = $('#otp-input').val();    // grab the content that user inputs
        console.log(otpInput);
        if ($.trim(otpInput) == '') {            // if the input message is empty
            return false;
        }
        
        callOTPApi(otpInput)                     // call api to send msg
            .then((response) => {
                console.log(response);          // log the response
                var data = response.data;       // get the response from backend
                console.log("data");
                console.log(data);
                
                if (data.Count && data.Count > 0) {
                    console.log('success');
                    $('.success').removeClass("hide");
                    $('.failure').addClass("hide");
                    var item = data.Items[0]
                    console.log(item.name);
                    //$('<span>Hello '+item.name+'</span>').appendTo($('.greeting'))
                    $('.greeting').html('<span>Hello '+item.name+'</span>');
                } else {                        // handle empty response
                    console.log('access denied');
                    $('.failure').removeClass("hide");
                    $('.success').addClass("hide");
                    $('.greeting').addClass("hide");
                    $('.greeting').html('');
                }
            }).
        catch((error) => {
            console.log('getting response error', error);
        });
    }

    // if the user hits otp-submit button, call submitOTP
    $('.otp-submit').click(function () {
        console.log("opt-submit hit");
        //e.preventDefault();
        submitOTP();
    });

});