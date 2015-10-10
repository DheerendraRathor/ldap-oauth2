/**
 * Created by dheerendra on 10/10/15.
 */

var iframe_base_url = '//gymkhana.iitb.ac.in/sso/widget/login/?';

function SSO_JS(config) {
    'use strict';

    this.config = config || {};

    this._applyDefaults = function (conf) {
        this.config.response_type = this.config.hasOwnProperty('response_type') ? conf.response_type : 'code';
        this.config.scope = this.config.hasOwnProperty('scope') ? conf.scope : ['basic'];
        this.config.new_window = this.config.hasOwnProperty('new_window') ? conf.new_window : 'false';
        this.config.sso_root = this.config.hasOwnProperty('sso_root') ? conf.sso_root : document.getElementById('sso-root');
        this.config.sso_iframe = this.config.hasOwnProperty('sso_iframe') ? conf.sso_iframe : document.getElementById('sso_iframe');
    };

    this._scopeListToString = function () {
        var scope_string = '';
        this.config.scope.map(function (scope) {
            scope_string += scope + ' ';
        });
        scope_string = scope_string.replace(/\s+$/, '');
        this.config.scope = scope_string;
    };

    this._verify = function () {
        if (!this.config.hasOwnProperty('client_id')) {
            throw new Error('client_id is not provided');
        }
    };

    this._configToQuery = function () {
        var query_params = [];
        ['client_id', 'response_type', 'redirect_uri', 'scope', 'new_window'].map(
            function (config_str) {
                if (this.config.hasOwnProperty(config_str)) {
                    query_params.push(config_str + '=' + this.config[config_str]);
                }
            }.bind(this));
        return query_params.join('&');
    };

    this.render = function () {
        this._applyDefaults(this.config);
        this._scopeListToString();
        this._verify();
        var query = this._configToQuery();
        var iframe_url = iframe_base_url + query;

        var iframe = document.createElement('iframe');
        iframe.setAttribute('id', 'sso_iframe');
        iframe.setAttribute('src', iframe_url);
        iframe.setAttribute('frameBorder', '0');
        iframe.setAttribute('scrolling', 'No');
        this.config.sso_root.appendChild(iframe);

        return this;
    };
}

var sso_root = new SSO_JS();

var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
var eventer = window[eventMethod];
var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";

eventer(messageEvent, function (event) {
    var message = event.data;
    message = message.split('://');
    var protocol = message[0];
    if (protocol != 'sso-iframe') {
        return;
    }
    var dimensions = message[1].split(':');

    sso_root.config.sso_iframe.height = dimensions[0] + 'px';
    sso_root.config.sso_iframe.width = dimensions[1] + 'px';
}, false);
