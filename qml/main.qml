import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Controls.Material
import Searcher

ApplicationWindow {
    id: window
    width: 400
    height: 500
    visible: true
    title: qsTr("Scavenger")
    //flags: Qt.FramelessWindowHint

    /*Component.onCompleted: {
        var component = Qt.createComponent("result_viewer.qml")
        if(component.status == Component.Error) {
            console.debug("Error:" + component.errorString());
            return
        }
        var win = component.createObject()
        win.show()
    }*/

    Material.theme: Material.Dark
    Material.accent: Material.LightBlue

    TextField {
        id: searchField
        width: 300
        text: qsTr("")
        selectByMouse: true
        placeholderText: qsTr("Search with Scavenger")
        verticalAlignment: Text.AlignVCenter
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 60
    }

    Timer {
        property var card_component: Qt.createComponent("card.qml")

        interval: 1
        running: true
        repeat: true
        onTriggered: {
            searcher.query = searchField.text

            let search_results = searcher.search_results
            if(!searcher.results_have_changed) {
                return
            }
            searcher.results_have_changed = false

            searcher.cards.forEach((card) => {
                card.destroy()
            })
            searcher.cards = []

            let last_added_card
            let cards_added = []
            let new_window_height = searchField.height
            search_results.forEach((search_result) => {

                let parent = last_added_card ? last_added_card : searchField

                last_added_card = card_component.createObject()
                last_added_card.parent = parent
                last_added_card.title = search_result['title']
                last_added_card.preview = search_result['preview']
                last_added_card.token = search_result['token']
                
                cards_added.push(last_added_card)
                new_window_height += last_added_card.height + last_added_card.anchors.topMargin + last_added_card.anchors.bottomMargin
            })

            searcher.cards = cards_added

            window.height = new_window_height;
        }
    }

    Searcher {
        id: searcher
    }
}
