jQuery.noConflict();

function gs_profile_invite_respond_init() {
    jQuery("#form\\.password1").focus();

    jQuery("#privacy-button").click( function () {
        var uri = "/policies/privacy/ #privacy";
        jQuery("#privacy-content").load(uri);
    });
    
    jQuery("#tc-button").click( function () {
        var uri = "/policies/aup/ #aup";
        jQuery("#tc-content").load(uri);
    });
}

jQuery(window).load( gs_profile_invite_respond_init );
