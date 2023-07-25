window.onload = () => {
    //Init responsivness
    InitResponsive();
    //Navigate to the currently opened document
    Navigate();
    //Generate sections of the document
    RenderSections();
};

/*
================================================
|                                              |
|                 Responsivity                 |
|                                              |
================================================
*/

const screen_sizes = [0, 576, 768, 992, 1200];
const screen_sizes_names = ['xs', 'sm', 'md', 'lg', 'xl'];
let screen_lastState = -1;
let repsonsive_screen = null;

const UpdateScreenSize = () => {
    const oldState = screen_lastState;
    const w = document.body.clientWidth;
    let i = screen_sizes.length;
    while(--i > -1)
        if(w >= screen_sizes[i])
            break;
    if(screen_lastState != i){
        screen_lastState = i;
        //update responsive-screen
        if(repsonsive_screen){
            i = repsonsive_screen.length;
            while(--i > -1){
                //remove old class
                if(oldState != -1)
                    repsonsive_screen[i].classList.remove('screen-' + screen_sizes_names[oldState]);
                //add new class
                repsonsive_screen[i].classList.add('screen-' + screen_sizes_names[screen_lastState]);
            }
        }
    }    
};

const InitResponsive = () => {
    repsonsive_screen = document.getElementsByClassName('responsive-screen');
    if(repsonsive_screen.length == 0)
        repsonsive_screen = null;
    const e = () => {
        UpdateScreenSize();
    };
    window.addEventListener("resize", e);
    e();
};

/*
================================================
|                                              |
|                  Navigation                  |
|                                              |
================================================
*/

const ToggleFolder = (header) => {
    header = header.parentNode;
    //css
    header.classList.toggle('folder-opened');
    //hide/show
    header = header.lastElementChild;
    header.hidden = !header.hidden;
};

const Navigate = () => {
    console.log(window.location.pathname);
};

/*
================================================
|                                              |
|                 Mobile Burger                |
|                                              |
================================================
*/

const MobileBurgerClick = () => {
    const mobileNavbar = document.getElementById('mobile-navbar');
    const panelLeft = document.getElementById('panel-left');
    const panelMiddle = document.getElementById('panel-middle');
    if(mobileNavbar.classList.contains('mobile')){
        panelLeft.classList.remove('mobile');
        mobileNavbar.classList.remove('mobile');
        panelMiddle.classList.remove('mobile');
    }else{
        panelLeft.classList.add('mobile');
        mobileNavbar.classList.add('mobile');
        panelMiddle.classList.add('mobile');
    }
};

/*
================================================
|                                              |
|                   Sections                   |
|                                              |
================================================
*/

const RenderSections = () => {
    
};