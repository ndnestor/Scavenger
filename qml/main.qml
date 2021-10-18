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

                last_added_card = Qt.createQmlObject(`
                    import QtQuick;
                    Rectangle {
                        color: "black";
                        width: window.width;
                        height: 40;
                        anchors.horizontalCenter: parent ? parent.horizontalCenter : undefined;
                        anchors.top: parent ? parent.bottom : undefined;
                        anchors.topMargin: 2;

                        Text {
                            text: qsTr("${search_result['title']}");
                            anchors.horizontalCenter: parent ? parent.horizontalCenter : undefined;
                            anchors.top: parent ? parent.top : undefined;
                            anchors.topMargin: 5;
                            horizontalAlignment: Text.AlignHCenter;
                            verticalAlignment: Text.AlignVCenter;
                            color: "white";
                            font.pointSize: 10;
                        }

                        Text {
                            text: qsTr("${search_result['preview']}");
                            anchors.horizontalCenter: parent ? parent.horizontalCenter : undefined;
                            anchors.bottom: parent ? parent.bottom : undefined;
                            anchors.bottomMargin: 5;
                            horizontalAlignment: Text.AlignHCenter;
                            verticalAlignment: Text.AlignVCenter;
                            color: "white";
                            font.pointSize: 10;
                        }
                    }`, parent)
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
