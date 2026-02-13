bates_analytics = window.bates_analytics || {};

if( typeof bates_analytics.getCookies === 'undefined' ) {
	bates_analytics.getCookies = function() {
		var c = document.cookie.split(';');
		var out = {};
		if( c.length < 1 )
			return out;
		c.forEach( pair => {
			pair = pair.trim();
			pair = pair.split('=')
			let val = (pair.length > 1) ? pair[1] : true;
			out[ pair[0] ] = val;
		})
		return out;
	};
}

const matchesUrlParam = function( keysToCheck ) {
	if( window.location.search == '' )
		return false;
	var queryParams = new URLSearchParams(window.location.search);
	for( let paramKey in keysToCheck ) {
		// if one of our specified query params is present in the url
		if( queryParams.has( paramKey ) ) {
			// if we've specified true for the param value match just existance, 
			// otherwise, see if our specified value matches the value in the url
			if ( 
				keysToCheck[paramKey] === true
				||
				keysToCheck[paramKey] == queryParams.get( paramKey ) 
			) {
				// if our query param matches
				return true
			}
		}
	}
	return false;
};

const shouldWeTag = function(){

	/**
	 * To track a domain, set the domain (optionally include the subdomain) as the object key name,
	 * 
	 * To track the whole domain/subdomain, set the value to 1
	 * 
	 * To only track part of a domain, set the value to an object with the following entries:
	 * 
	 * @key default [int]			1 or 0, whether to track this domain in general (if no exceptions match)
	 * @key exceptions [array]: 	an array of exception objects: each objects must have an allow key, and 
	 * 								at least a "path" or "params" key, but it can have both. If you provide 
	 * 								both, both must match for the "allow" value to be used.
	 * 			@key allow [int]		1 or 0, whether to track this matched path/url
	 * 			@key path [string]		A path to match against
	 * 			@key params [object]	Key/value pairs to match against url parameters. If you just
	 * 									want to match the key, set the value to true
	 */
	const hostMap = {
		"abacus.bates.edu": {
			"exceptions": [
				{
					path: '/oralhistory/',
					allow: 1,
				}
			],
		},
		"adminlb.imodules.com":1,
		"archives.bates.edu": {
			"default": 0,
			"exceptions": [
				{
					path: '/photos/',
					allow: 1,
				}
			],
		},

		// keeping the various catalog urls together
		"catalog.bates.edu":1,
		"catalog-archive.bates.edu":1,
		"batescollege.coursedog.com":1,
		"batescatalogpreview.coursedog.com":1,
		"bates-catalog.coursedog.com":1,

		"apply.bates.edu": {
			"default": 1,
			"exceptions": [
				{
					path: "/account/login",
					params: {
						e: true,
					},
					allow: 0,
				},
			],
		},
		"bates-archives.libraryhost.com":1,
		"bates-college-store.myshopify.com":1,
		"bates.beta.libguides.com":1,
		// "bates.loc":1, // local testing environment
		"batescollege.tumblr.com":1,
		"batesnews.tumblr.com":1,
		"batesorientation2014.sched.org":1,
		"batesshortterm.tumblr.com":1,
		"bco-dev.bates.edu":1,
		"bco-jparis.bates.edu":1,
		"bco-kblake.bates.edu":1,
		"bco-nobrien.bates.edu":1,
		"bco-remodel.bates.edu":1,
		"bco-test.bates.edu":1,
		"coursedog.com":1,
		"community.bates.edu":1,
		"dexter.bates.edu":1,
		"digilib.bates.edu":1,
		"diversebookfinder.org":1,
		"cat.diversebookfinder.org":1,
		"emergency.bates.edu":1,
		"events.bates.edu":1,
		"events-test.bates.edu":1,
		"gg-bprod.bates.edu":1, 
		"giftplanning.bates.edu": 1,
		"illiad.bates.edu":1,
		"libanswers.bates.edu":1,
		"libguides.bates.edu":1,
		"lyceum-beta.bates.edu":1,
		"lyceum.bates.edu":1,
		"marchmania.org":1,
		"menu.bates.edu":1,
		"museum.bates.edu":1,
		"museum-dev.bates.edu":1,
		"new.livestream.com":1,
		"picturestories.bates.edu":1,
		"quad.bates.edu":1,
		"quad-dev.bates.edu":1,
		"quad-sa.bates.edu":1,
		"quad-test.bates.edu":1,
		"securelb.imodules.com":1,
		"store.bates.edu":1,
		"www-stage.bates.edu":1,
		"www.bates.edu":1,
		"www.batesdancefestival.org":1,
		"www.garnetgateway.com":1,
		"gobatesbobcats.com":1,
	};
	var out = 0,
		domain = window.location.host,
		path = window.location.pathname.toLowerCase();
	
	if( typeof hostMap[domain] === 'undefined' )
		return false;

	if( hostMap[domain] === 1 )
		return true;

	// check for exceptions, and change the default as needed
	if( typeof hostMap[domain] === 'object' ){

		// set our default if there is one
		if( typeof hostMap[domain].default != 'undefined' )
			out = hostMap[domain].default ;

		if( typeof hostMap[domain].exceptions !== 'undefined' ) {
			hostMap[domain].exceptions.forEach( exception => {

				// if a path exception exists
				if( typeof exception.path !== 'undefined' ) {
					// match our path with front of object key
					if( exception.path.indexOf( path ) === 0 ) {
						// if we've also specified a query param to check by, check that
						if( typeof exception.params !== 'undefined' ) {
							if( matchesUrlParam( exception.params ) ) {
								// if our query param matches, use the "allow" value
								out = exception.allow;
							}
						// if we haven't specified a query param to check by, just use the "allow" value now
						} else {
							out = exception.allow;
						}
					}
				
				// if ONLY a params exception exists
				} else if( typeof exception.params !== 'undefined' ) {
					if( matchesUrlParam( exception.params ) ) {
						// if our query param matches, use the "allow" value
						out = exception.allow;
					}
				}
			});
		}
	}
	return (out==1);
};

if( shouldWeTag() ) {

	// Our own FB conversions api implementation
	(function(){
		var myself, a, path, thisUrlPath, event_id;
		// Get our own uri directory
		myself = document.querySelector('script[src*="/analytics.js"');
		if( ! myself )
			return;

		const createEventId = () => Math.floor(Math.random()*999999999999);

		a = new URL( myself.src );
		if( a.pathname === '/') {
			path = '/';
		} else {
			// path = /analytics/analytics.js?v=1.2.3
			path = a.pathname.split('/');
			// path = ['', 'analytics', 'analytics.js?v=1.2.3' ]
			path.pop();
			// path = ['', 'analytics']
			path = path.join('/') + '/';
			// path = /analytics/
		}
		thisUrlPath = a.origin + path;

		var newParams = new URLSearchParams();
		var currentParams = new URLSearchParams( window.location.search )

		// create an event_id for deduping js & php event
		if( ! bates_analytics.FACEBOOK_ANALYTICS_EVENTS ) {
			bates_analytics.FACEBOOK_ANALYTICS_EVENTS = {};
		}
		
		const fbEvents = [
			'ViewContent',
			'Lead',
			'CompleteRegistration',
			// 'PageView'
		];

		fbEvents.forEach( eventName => {
			if( typeof bates_analytics.FACEBOOK_ANALYTICS_EVENTS[eventName] === 'undefined' )
				bates_analytics.FACEBOOK_ANALYTICS_EVENTS[eventName] = createEventId();
			// save event_id so the js pixel implementation can use it later
			newParams.set(`${eventName}_event_id`, bates_analytics.FACEBOOK_ANALYTICS_EVENTS[eventName] );
		});
		
		newParams.set('theurl', window.location);

		// Get facebook's meta pixel set cookies
		// More details: https://developers.facebook.com/docs/marketing-api/conversions-api/parameters/fbp-and-fbc
		var cookies = bates_analytics.getCookies();
		if( typeof cookies._fbp !== 'undefined' ) {
			newParams.set('fbp', cookies._fbp );
		}
		if( typeof cookies._fbc !== 'undefined' ) {
			newParams.set('fbc', cookies._fbc)
		} else if ( currentParams.has('fbclid') ) {
			newParams.set('fbclid', currentParams.get('fbclid') );
		}

		const fetchUrl = thisUrlPath + 'fbconv.php?' + newParams.toString();

		// for now, don't grab the response
		fetch( fetchUrl );
	})();


	// Tag Manager 
	(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start': new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer', "GTM-NS4K3BT" ) 
}
