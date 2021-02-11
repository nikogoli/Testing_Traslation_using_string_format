import bpy

from bpy.props import *

bl_info = {
	"name": "Translation Test",
	"author": "nikogoli",
	"version": (0, 1),
	"blender": (2, 91, 0),
	"location": "None",
	"description": "Translation Test",
	"warning": "",
	"support": "TESTING",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Custom"
}


# 翻訳用辞書
translation_dict = {
	"en_US" :{
		("*", "1: Active Object is %s") : "1: Active Object is %s",
		("*", "2: Active Object is {}") : "2: Active Object is {}",
		("*", 'f"3: Active Object is {name}"') : 'f"3: Active Object is {name}"',
		("*", "4: Active Object is {name}") : "4: Active Object is {name}",
		},
	"ja_JP" :
		{
		("*", "1: Active Object is %s") : "1: アクティブオブジェクトは %s です",
		("*", "2: Active Object is {}") : "2: アクティブオブジェクトは {} です",
		("*", 'f"3: Active Object is {name}"') : 'f"3: アクティブオブジェクトは {name} です"',
		("*", "4: Active Object is {name}") : "4: アクティブオブジェクトは {name} です",
		}
}



# 言語の切替用オペレーター
class ToggleInterfaceLanguage(bpy.types.Operator):
	bl_idname = "wm.toggle_interface_language"
	bl_label = "Switch UI Language (English/Japanese)"
	bl_description = "Switch interface language between English and Japanese"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		if (bpy.context.preferences.view.language == "en_US"):
			bpy.context.preferences.view.language = "ja_JP"
		elif (bpy.context.preferences.view.language == "ja_JP"):
			bpy.context.preferences.view.language = "en_US"
		return {'FINISHED'}


# アドオン設定
class AddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__

	def draw(self, context):
		layout = self.layout
		layout.operator(ToggleInterfaceLanguage.bl_idname)
		name = context.active_object.name

		box = layout.box()
		box.label(text="name = context.active_object.name")
		box.label(text='翻訳辞書その1：  "1: Active Object is %s"　→　"1: アクティブオブジェクトは %s です"')
		box.label(text='翻訳辞書その2：  "2: Active Object is {}"　→　"2: アクティブオブジェクトは {} です"')
		box.label(text='翻訳辞書その3：  \'f"3: Active Object is {name}"\'　→　\'f"3: アクティブオブジェクトは {name} です"\'')
		box.label(text='翻訳辞書その4：  "4: Active Object is {name}"　→　"4: アクティブオブジェクトは {name} です"')

		box1 = layout.box()
		box1.label(text='%演算子を使う方法')
		box1.label(text='コード： text = bpy.app.translations.pgettext_iface( "1: Active Object is %s" ) % (name)')
		box1.label(text=bpy.app.translations.pgettext_iface(
				"1: Active Object is %s") % (name))

		box2 = layout.box()
		box2.label(text='str.format( )を使う方法')
		box2.label(text='コード： text = bpy.app.translations.pgettext_iface( "2: Active Object is {}" ).format(name)')
		box2.label(text=bpy.app.translations.pgettext_iface(
				"2: Active Object is {}").format(name))

		box3 = layout.box()
		box3.label(text='f文字列を使う方法その1：f"~"を直接記述し、全体を\' \'で囲む')
		box3.label(text='コード： text = eval( bpy.app.translations.pgettext_iface( \'f"3: Active Object is {name}"\' ) )')
		box3.label(text=eval(bpy.app.translations.pgettext_iface('f"3: Active Object is {name}"')))

		box4 = layout.box()
		box4.label(text='f文字列を使う方法その2：f"~"は記述せず、翻訳後に追加する')
		box4.label(text='コード： text = eval( f\' f"{ bpy.app.translations.pgettext_iface( "4: Active Object is {name}" ) }" \' )')
		box4.label(text=eval(f'f"{bpy.app.translations.pgettext_iface("4: Active Object is {name}")}"'))


#---------------------------------------------------


classes = [
	ToggleInterfaceLanguage,
	AddonPreferences
]

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.app.translations.register(__name__, translation_dict)   # 辞書の登録

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)
	bpy.app.translations.unregister(__name__)   # 辞書の削除


if __name__ == "__main__":
	register()
