jQuery.noConflict();

function gs_profile_invite_respond_password_init () {
    var toggler = null;
    toggler = GSProfilePasswordToggle('#form\\.password1', 
                                      '#gs-profile-invite-respond-password-set-toggle-widget');
}

function gs_profile_invite_respond_init () {
    jQuery("#form\\.password1").focus();

    jQuery("#privacy-button").click( function () {
        var uri = "/policies/privacy/ #privacy";
        jQuery("#privacy-content").load(uri);
    });
    
    jQuery("#tc-button").click( function () {
        var uri = "/policies/aup/ #aup";
        jQuery("#tc-content").load(uri);
    });
    gsJsLoader.with_module('/++resource++gs-profile-password-toggle-min-20130516.js',
                           gs_profile_invite_respond_password_init);            
}

jQuery(window).load( gs_profile_invite_respond_init );
