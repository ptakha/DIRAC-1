=========
Tab theme
=========

In this section a detailed description of the Tab theme is presented:

    - `Main panel`_
    - `Menu structure`_
    - `Manage application and desktop`_
    - `Share application and desktop`_
    - `Settings panel`_

Main panel
----------


 The main panel consists of two widget:
   1. Menu 
   2. Desktop

.. image:: images/maintab.png
   :scale: 30 %
   :alt: Tab theme main view.
   :align: center


**Menu**

 It contains three main menu:

.. image:: images/menus.png
   :scale: 50 %
   :alt: main menus
   :align: center

#. It is the Intro panel
#. It is the Main panel
#. You can found more information about DIRAC.

The default is 2. You can change by clicking on the icons.

**Desktop**

 It is a container which contains various applications on different desktops.



Menu structure
--------------

 Menu consists of two widgets:
   #. Desktops&Applications
   #. Settings
   
.. image:: images/menustructure.png
   :scale: 50 %
   :alt: menu structure
   :align: right
   
**Desktop&Applications**

 You can manage your applications and desktops. The menu structure:
   * Web : it contains external links
   * Tools : You can found DIRAC specific applications.
   * Applications: You can found DIRAC and VO specific applications.
   * OldPortal: It is link to the old portal.
   * DIRAC it is an external link to DIRAC portal
   * My Desktops it is contains all saved desktops. You can see a **Default** desktop which contains all applications which belongs to the **Default** desktop. 
   * Shared: It contains all Shared desktops and applications.
   

Manage application and desktop
------------------------------

You can manage the state of applications and desktops by by clicking to the following menu.

.. image:: images/managemenuitems.png
   :scale: 50 %
   :alt: Applications and more
   :align: center

**Desktop**

The Desktop menu item contains:

   * New Desktop: You can create an empty desktop.
   * Save: You can save the desktop
   * Save As you can duplicate your desktop.
   * Delete You can delete different desktops.

If you click on the delete menu item, a pop up window will appear:    

.. image:: images/delete.png
   :scale: 50 %
   :alt: Delete menu
   :align: center

You can select the desktops to be deleted.

**Application**

The Application menu item contains:
   * Save
   * Save As
   * Delete
 
 These menu items have the same functionalities as the Desktop menu items.
 
**Context menu**

You have another possibility to manage applications and desktops. You have to right click on the application/desktop
what you want to modify.

.. image:: images/contextmenu.png
   :scale: 50 %
   :alt: Context menu
   :align: center

You have few additional menu items:
   * Make public: Used to make public an application/desktop to everyone. 
   * Share desktop: Used to share the desktop within a specific user.
   * Share application: Used to share the application within a specific user.
   * Make private: revoke the access to the desktop/application.
   * Switch to presenter view: The applications will be open in a single desktop.
   * Switch to tab view: The applications opened in different tabs.
   
**Presenter view**

The application which belongs to a desktop will be opened in a single tab. You can change the layout of the desktop using the buttons in the right corner of the panel (The buttons are in the red rectangle).  

.. image:: images/presenterview.png
   :scale: 30 %
   :alt: Presenter view
   :align: center

**Tab view**

The applications within a desktop will be opened in different tab.

.. image:: images/tabview.png
   :scale: 30 %
   :alt: Tab view
   :align: center

In the right corner of the Tab theme you can see two icons.

*First icon* You can access to a specific application by clicking on the first icon. This is very useful when you have lot of application open in a desktop.

.. image:: images/tabmenu.png
   :scale: 30 %
   :alt: Tab menu
   :align: center


*Second icon* You can write help to the current application. 

.. image:: images/helpmenu.png
   :scale: 30 %
   :alt: Help menu
   :align: center

Share application and desktop
-----------------------------

The applications/desktops can be shared. You can share an application/desktop by right click on the application/desktop what 
you want to share (more information above in the `Manage application and desktop`_).

**Share an application/desktop**

You have to do the following steps to share an application/desktop:
   #. right click on the desktop/application what you want to share.
   #. choose the menu item: Share desktop or Share Application.
   #. copy the text (for example: desktop|zmathe|lhcb_prmgr|JobMonitorAll) and click OK on the pop up window:
   #. send the text (desktop|zmathe|lhcb_prmgr|JobMonitorAll) to the person

.. image:: images/share.png
   :scale: 50 %
   :alt: Share message box.
   :align: center
   
**Load a shared application or desktop**   
   
You have to use the *State Loader* menu item:

.. image:: images/stateloader.png
   :scale: 50 %
   :alt: State loader.
   :align: center

The State Loader widget is the following:

.. image:: images/loader.png
   :scale: 50 %
   :alt: Loader.
   :align: center

You have to provide the Shared State (for example: desktop|zmathe|lhcb_prmgr|JobMonitorAll) and a name (for example: newName).
You have tree different way to load a shared state:

   #. Load
   #. Create Link
   #. Load & Create Link
   
**Load**

If you click on Load, you load the shared desktop/application to you desktop. The name of the application will be the provided name. For example: newName.

.. image:: images/loaddesktop.png
   :scale: 30 %
   :alt: Loaded desktop.
   :align: center


**Create Link**

This save the application/desktop *Shared* menu item. Which mean it keeps a pointer(reference) to the original desktop/application. 
This will not load the application/desktop into your desktop.

.. image:: images/createlink.png
   :scale: 50 %
   :alt: Create link.
   :align: center



**Load & Create Link**

The desktop/application will be loaded to your desktop and it is saved under the **Shared** menu item. 

**Delete shared applications/desktops**

You have to click on the menu `Manage application and desktop`_ and then select application or desktop depending what you want to delete. 
For example: Let's delete the **newName** shared desktop.

.. image:: images/deletelink.png
   :scale: 50 %
   :alt: Delete link.
   :align: center  

You have to select what you want to delete state or a link. As it is a shared desktop what we want to delete we have to select *Links*. 
You have to click on the Delete button.

Settings panel
--------------

In the settings panel you can set up your portal. 
You have to click on the **Settings** widget:

.. image:: images/settings.png
   :scale: 50 %
   :alt: Settings.
   :align: center  


.. image:: images/settingspanel.png
   :scale: 50 %
   :alt: Settings panel.
   :align: center  

You can define the following:
      * Group you can change the role
      * Setup: you can switch between different setups.
      * Theme you can change the look and feel and also you can switch between Tab and Desktop themes.
       
We have 3 look and feels:
   #. Grey it is the default
   #. Neptune
   #. Classic

You can automatically change the applications using *Automatic tab change* Note: After you set it you have to save the desktop. 
Consequently, you can not have automatic tab change in the *Default* desktop. 
    
**Grey**

.. image:: images/grey.png
   :scale: 30 %
   :alt: Grey look and feel.
   :align: center  


**Neptune**

.. image:: images/neptune.png
   :scale: 30 %
   :alt: Neptune look and feel.
   :align: center  


**Classic**

.. image:: images/classic.png
   :scale: 30 %
   :alt: Classic look and feel.
   :align: center  

