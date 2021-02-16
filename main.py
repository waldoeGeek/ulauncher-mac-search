from src.mac import Vendor
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction


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
            # if mac_list['vendor'] == 'Not Found!':
            #     pass
            # else:
            #     url = mac_list['url']
            #     items.append(ExtensionResultItem(
            #         icon='images/success_icon.png',
            #         name=mac_list['vendor'],
            #         description=query,
            #         on_enter=OpenUrlAction(url)
            #     ))

            for result in mac_list:
                url = mac_list[0]['url']
                vendor = mac_list[0]['vendor']
                if vendor == 'Not Found!':
                    items.append(ExtensionResultItem(icon='images/error_icon.png',
                                                     name=vendor,
                                                     description=query,
                                                     on_enter=HideWindowAction()))
                else:
                    # url = mac_list['url']
                    items.append(ExtensionResultItem(
                        icon='images/success_icon.png',
                        name=vendor,
                        description=query,
                        on_enter=OpenUrlAction(url),
                        on_alt_enter=CopyToClipboardAction(url)
                        # on_enter=HideWindowAction()
                    ))
                                                     # on_enter=HideWindowAction()))

            return RenderResultListAction(items)
            import ipdb; ipdb.set_trace()
        except Exception as e:
            items.append(ExtensionResultItem(icon='images/error_icon.png',
                                             name='ERROR',
                                             description='No items Found!',
                                             on_enter=HideWindowAction()))

            return RenderResultListAction(items)


if __name__ == '__main__':
    DemoExtension().run()
