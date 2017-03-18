jQuery(document).ready(function($){
	var secondaryNav = $('.cd-secondary-nav'),
		secondaryNavTopPosition = secondaryNav.offset().top,
		taglineOffesetTop = $('#cd-intro-tagline').offset().top + $('#cd-intro-tagline').height() + parseInt($('#cd-intro-tagline').css('paddingTop').replace('px', '')),
		contentSections = $('.cd-section');
	
	$(window).on('scroll', function(){
		//on desktop - assign a position fixed to logo and action button and move them outside the viewport
		( $(window).scrollTop() > taglineOffesetTop ) ? $('#cd-logo, .cd-btn').addClass('is-hidden') : $('#cd-logo, .cd-btn').removeClass('is-hidden');
		
		//on desktop - fix secondary navigation on scrolling
		if($(window).scrollTop() > secondaryNavTopPosition ) {
			//fix secondary navigation
			secondaryNav.addClass('is-fixed');
			//push the .cd-main-content giving it a top-margin
			$('.cd-main-content').addClass('has-top-margin');	
			//on Firefox CSS transition/animation fails when parent element changes position attribute
			//so we to change secondary navigation childrens attributes after having changed its position value
			setTimeout(function() {
	            secondaryNav.addClass('animate-children');
	            $('cd-btn').addClass('slide-in');
				$('.cd-btn').addClass('slide-in');
	        }, 50);
		} else {
			secondaryNav.removeClass('is-fixed');
			$('.cd-main-content').removeClass('has-top-margin');
			setTimeout(function() {
	            secondaryNav.removeClass('animate-children');
	            $('#cd-logo').removeClass('slide-in');
				$('.cd-btn').removeClass('slide-in');
	        }, 50);
		}

		//on desktop - update the active link in the secondary fixed navigation
		updateSecondaryNavigation();
	});

	function updateSecondaryNavigation() {
		contentSections.each(function(){
			var actual = $(this),
				actualHeight = actual.height() + parseInt(actual.css('paddingTop').replace('px', '')) + parseInt(actual.css('paddingBottom').replace('px', '')),
				actualAnchor = secondaryNav.find('a[href="#'+actual.attr('id')+'"]');
			if ( ( actual.offset().top - secondaryNav.height() <= $(window).scrollTop() ) && ( actual.offset().top +  actualHeight - secondaryNav.height() > $(window).scrollTop() ) ) {
				actualAnchor.addClass('active');
			}else {
				actualAnchor.removeClass('active');
			}
		});
	}

	//on mobile - open/close secondary navigation clicking/tapping the .cd-secondary-nav-trigger
	$('.cd-secondary-nav-trigger').on('click', function(event){
		event.preventDefault();
		$(this).toggleClass('menu-is-open');
		secondaryNav.find('ul').toggleClass('is-visible');
	});

	//smooth scrolling when clicking on the secondary navigation items
	secondaryNav.find('ul a').on('click', function(event){
        event.preventDefault();
        var target= $(this.hash);
        $('body,html').animate({
        	'scrollTop': target.offset().top - secondaryNav.height() + 1
        	}, 400
        ); 
        //on mobile - close secondary navigation
        $('.cd-secondary-nav-trigger').removeClass('menu-is-open');
        secondaryNav.find('ul').removeClass('is-visible');
    });

    //on mobile - open/close primary navigation clicking/tapping the menu icon
	$('.cd-primary-nav').on('click', function(event){
		if($(event.target).is('.cd-primary-nav')) $(this).children('ul').toggleClass('is-visible');
	});
});

function saveEdits() {
    //get the editable elements.
    var editElems = {
        'tn': document.getElementById('tn').innerHTML,
        'cn': document.getElementById('cn').innerHTML,
		'edit': document.getElementById('edit').innerHTML
    };

    //save the content to local storage. Stringify object as localstorage can only support string values
    localStorage.setItem('userEdits', JSON.stringify(editElems));
}
function checkEdits(){
    //find out if the user has previously saved edits
    var userEdits = localStorage.getItem('userEdits');
    if(userEdits){
        userEdits = JSON.parse(userEdits);
        for(var elementId in userEdits){
          document.getElementById(elementId).innerHTML = userEdits[elementId];
        }
    }
}		

// slideup/slidedown
  trigger = function () {
  Slider.classList.toggle("slide-down")
  //Slider.classList.toggle("slideup")
};


// Code goes here
window.onload = function() {
  function addAct(nameact, when, where,desc) {
    var buses = document.querySelectorAll(".bus");
    var curr = document.createElement("div");
    curr.setAttribute("class", "name");
    var p0 = document.createElement("p");
    p0.setAttribute("class", "nameact");
    p0.innerHTML = nameact;
    var p1 = document.createElement("p");
    p1.setAttribute("class", "whereisit");
    p1.innerHTML = when;
    var p2 = document.createElement("p");
    p2.setAttribute("class", "when");
    p2.innerHTML = where;
	var p3 = document.createElement("p");
    p3.setAttribute("class", "describtion");
    p3.innerHTML = desc;
    curr.appendChild(p0);
    curr.appendChild(p1);
    curr.appendChild(p2);
	  curr.appendChild(p3);
    if (buses.length) {
      buses[buses.length -1].insertAdjacentHTML("afterEnd", curr.outerHTML)
    } else {
      document.forms[0].insertAdjacentHTML("afterEnd", curr.outerHTML)
    }
  }

  var obj = {nameact: "", when: "", where: "",desc:""};

  document.forms[0].onchange = function(e) {
    obj[e.target.name] = e.target.value;
  }

  document.forms[0].onsubmit = function(e) {
    e.preventDefault();
    addAct(obj.nameact, obj.when, obj.where, obj.desc)
  }
}
