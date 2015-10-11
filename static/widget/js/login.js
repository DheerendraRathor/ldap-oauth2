/**
 * Created by dheerendra on 10/10/15.
 * SSO_JS - v2.0 - 12-10-2015
 */

function SSO_JS(init) {
    'use strict';

    this.iframe_base_url = '//gymkhana.iitb.ac.in/sso/widget/login/?';

    this.iframe = null;

    this.config = init.config || {};

    this.config_keys = [
        'client_id',
        'response_type',
        'redirect_uri',
        'scope',
        'state',
        'new_window'
    ];

    this.colors = init.colors || {};

    this.color_keys = [
        'button_div_bg_color',
        'button_anchor_color',
        'logout_anchor_color'
    ];

    this.init = function () {
        this._setupMessageListener();
        return this._render();
    };

    /**
     * @deprecated Will be removed in future versions. Use init() instead
     */
    this.render = function () {
        console.warn('render() function will be removed in future versions. Use init() instead');
        return this.init();
    };

    this._render = function () {
        this._applyDefaults(this.config);
        this._scopeListToString();
        this._verify();
        this._verifyColors();
        var query = this._dictsToQueryParam(
            [
                [this.config_keys, this.config],
                [this.color_keys, this.colors]
            ]
        );
        var iframe_url = this.iframe_base_url + query;

        this.iframe = document.createElement('iframe');
        this.iframe.setAttribute('id', 'sso-iframe');
        this.iframe.setAttribute('src', iframe_url);
        this.iframe.setAttribute('frameBorder', '0');
        this.iframe.setAttribute('scrolling', 'No');
        this.iframe.setAttribute('height', '70px');
        this.iframe.setAttribute('width', '200px');
        this.config.sso_root.appendChild(this.iframe);

        return this;
    };

    this._verifyColors = function () {
        var hex_pattern = /^(?:[0-9a-fA-F]{3}){1,2}$/;
        this.color_keys.map(function (color) {
            if (this.colors.hasOwnProperty(color)) {
                if (!hex_pattern.test(this.colors[color])) {
                    throw new Error('Color ' + color + ' must be a valid HEX with #');
                }
            }
        }.bind(this));
    };

    this._applyDefaults = function (conf) {
        this.config.response_type = this.config.hasOwnProperty('response_type') ? conf.response_type : 'code';
        this.config.scope = this.config.hasOwnProperty('scope') ? conf.scope : ['basic'];
        this.config.new_window = this.config.hasOwnProperty('new_window') ? conf.new_window : 'false';
        this.config.sso_root = this.config.hasOwnProperty('sso_root') ? conf.sso_root : document.getElementById('sso-root');
    };

    this._scopeListToString = function () {
        this.config.scope = this.config.scope.join(' ');
    };

    this._verify = function () {
        if (!this.config.hasOwnProperty('client_id')) {
            throw new Error('client_id is not provided');
        }
    };

    /**
     * This function converts a list of dictionaries into single HTTP GET query param
     * However list of dictionaries should be a list of of [keys, dict] where keys is list subset
     * of keys of dict which should be included in query param
     * @param dicts list of list [[['a', 'b], {'a': 1, 'b': 2}], ]
     * @private
     */
    this._dictsToQueryParam = function (dicts) {
        var query_params = [];
        dicts.map(function (keys_dict_pair) {
            keys_dict_pair[0].map(function (key) {
                if (keys_dict_pair[1].hasOwnProperty(key)) {
                    query_params.push(key + '=' + keys_dict_pair[1][key]);
                }
            });
        });
        return query_params.join('&');
    };

    this._setupMessageListener = function () {
        var eventMethod = window.addEventListener ? "addEventListener" : "attachEvent";
        var eventer = window[eventMethod];
        var messageEvent = eventMethod == "attachEvent" ? "onmessage" : "message";

        eventer(messageEvent, function (event) {
            if (this.iframe == null || this.iframe == undefined) {
                return;
            }
            if (this.iframe.src.indexOf(event.origin) != 0){
                return;
            }
            var message = event.data;
            this._parseMessage(message);
        }.bind(this), false);
    };

    this._parseMessage = function (data) {
        var message = data.split('://');
        var protocol = message[0];
        if (protocol != 'sso-iframe') {
            return;
        }
        var dimensions = message[1].split(':');
        this._resizeIFrame(dimensions[0], dimensions[1]);
    };

    this._resizeIFrame = function (height, width) {
        this.iframe.height = height + 'px';
        this.iframe.width = width + 'px';
    };

}

var sso_root = new SSO_JS({});
