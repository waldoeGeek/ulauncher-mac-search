from src.mac import Vendor
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


mac = 'dc:71:96:2f:24:c5'
# search_url = 'https://hwaddress.com/?q=dc:71:96:2f:24:c4'

print(Vendor.search_vendor(mac))

class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        try:
            query = event.get_argument() or ""
            if len(query) < 6:
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon='images/searching_icon.png',
                        name="Keep Typing to search vendors ...",
                        on_enter=HideWindowAction(),
                        highlightable=False,
                    )
                ])

            query = Vendor.format_mac(query)
            # url = search_url + query
            mac_list = Vendor.search_vendor(query)
            for result in mac_list:
                if result == 'Not Found!':
                    items.append(ExtensionResultItem(icon='images/error_icon.png',
                                                     name=result,
                                                     description=query,
                                                     on_enter=HideWindowAction()))
                else:
                    items.append(ExtensionResultItem(
                        icon='images/success_icon.png',
                        name=result,
                        description=query,
                        on_enter=HideWindowAction()
                    ))
                                                     # on_enter=HideWindowAction()))

            return RenderResultListAction(items)
        except Exception as e:
            items.append(ExtensionResultItem(icon='images/error_icon.png',
                                             name='ERROR',
                                             description='No items Found!',
                                             on_enter=HideWindowAction()))

            return RenderResultListAction(items)


if __name__ == '__main__':
    DemoExtension().run()
